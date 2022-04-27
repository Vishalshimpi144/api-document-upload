from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    #This is completly optional, we can use the prefix in decorator as @router.get("/users")
    prefix="/lab",
    tags=['Lab']
)


@router.get("/", response_model=List[schemas.LabOut])
def get_all_lab(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    labs = db.query(models.Lab).all()
    return labs


@router.get("/{id}", response_model=List[schemas.LabOut])
def get_lab_by_id(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    lab = db.query(models.Lab).filter(models.Lab.id == id).first()

    if not lab:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lab with id : {id} not found")
    
    return lab

#POST: http://localhost/lab
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LabOut)
def create_lab(new_lab: schemas.CreateLab, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(new_lab)
    lab = models.Lab(created_by=current_user.id, **new_lab.dict())
    db.add(lab)
    db.commit();
    db.refresh(lab)
    return lab

#DELETE: http://localhost/lab/1
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 is not returning any data back to browser on deletion
async def delete_lab(id: int, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #deleting user
    lab_query = db.query(models.Lab).filter(models.Lab.id == id)
    lab = lab_query.first()
    
    if lab == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"lab with id: {id} does not exist")

    #if user.created_by != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                        detail="You are not authorize to perform requested opration")

    lab_query.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#PUT: http://localhost/lab/1
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_lab(id: int, updatelab: schemas.CreateLab, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    lab_query = db.query(models.Lab).filter(models.Lab.id == id)
    lab = lab_query.first()
    if lab == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Lab with id: {id} does not exist")

    lab_query.update(updatelab.dict(), synchronize_session=False)
    db.commit()
    return {"data": "Successfull"}
