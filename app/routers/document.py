from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.config import settings
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List
from app.core.s3_operations import S3


router = APIRouter(
    #This is completly optional, we can use the prefix in decorator as @router.get("/users")
    prefix="/document",
    tags=['Document']
)

s3 = S3()

#GET: http://localhost/document
@router.get("/", response_model=List[schemas.DocumentOut])
async def get_all_document(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    documents = db.query(models.Document).all() 
    return documents

#GET: http://localhost/document/1
@router.get("/{id}", response_model=schemas.DocumentOut)
async def get_document_by_id(id: int, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #imported Response, Status, HTTPException from FastAPI
    document = db.query(models.Document).filter(models.Document.id == id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"document with id: {id} does not found")
    return document


#POST: http://localhost/document
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DocumentOut)
def create_document(document: schemas.CreateDocument, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #print(document)
    new_document = models.Document(created_by=current_user.id, 
                                updated_by=current_user.id, 
                                document_code=document.document_code,
                                document_name=document.document_name,
                                parent_id=document.parent_id
                                )

    docuemnt_custom_name = s3.create_s3_custom_document_name(lab_name="test",
                                                                document_name=document.document_name)

    url, name = s3.upload_file_to_s3(aws_access_key_id=settings.s3_access_key, 
        bucketName=settings.s3_bucketname,
        aws_secret_access_key=settings.s3_secrete_access_key,
        name=docuemnt_custom_name,
        srcPath=document.srcPath
    )

    new_document.document_url = url
    new_document.s3_document_name = name

    db.add(new_document)
    db.commit();
    db.refresh(new_document)
    return new_document


#DELETE: http://localhost/document/1
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 is not returning any data back to browser on deletion
async def delete_document(id: int, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #deleting user
    document_query = db.query(models.Document).filter(models.Document.id == id)
    doc = document_query.first()
    
    if doc == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"doc with id: {id} does not exist")

    #if user.created_by != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                        detail="You are not authorize to perform requested opration")

    document_query.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#PUT: http://localhost/document/1
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_document(id: int, updateDocument: schemas.UpdateDocument, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document_query = db.query(models.Document).filter(models.Document.id == id)
    doc = document_query.first()
    print(doc)
    if doc == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"doc with id: {id} does not exist")

    docuemnt_custom_name = s3.create_s3_custom_document_name(lab_name="test",
                                                                document_name=updateDocument.document_name)

    url, name = s3.upload_file_to_s3(aws_access_key_id=settings.s3_access_key, 
        bucketName=settings.s3_bucketname,
        aws_secret_access_key=settings.s3_secrete_access_key,
        name=docuemnt_custom_name,
        srcPath=updateDocument.srcPath
    )

    doc.document_code=updateDocument.document_code
    doc.document_name=updateDocument.document_name
    doc.parent_id=updateDocument.parent_id
    doc.document_url=url
    doc.s3_document_name=name
    
    document_query.update(updateDocument.dict(), synchronize_session=False)
    db.commit()
    return {"data": "Successfull"}