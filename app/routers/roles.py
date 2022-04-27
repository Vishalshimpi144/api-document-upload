from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    #This is completly optional, we can use the prefix in decorator as @router.get("/users")
    prefix="/roles",
    tags=['Role']
)

#GET: http://localhost/roles
@router.get("/", response_model=List[schemas.RoleOut])
async def get_all_roles(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    roles = db.query(models.Roles).all() 
    return roles

#GET: http://localhost/roles/1
@router.get("/{id}", response_model=schemas.RoleOut)
async def get_role_by_id(id: int, db: Session =Depends(get_db), user_id: int = Depends(oauth2.get_current_user)): #imported Response, Status, HTTPException from FastAPI
    role = db.query(models.Roles).filter(models.Roles.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"role with id: {id} does not found")
    return role


#POST: http://localhost/roles
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RoleOut)
def create_role(new_role: schemas.CreateRole, db: Session =Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    role = models.Roles(**new_role.dict())
    db.add(role)
    db.commit();
    db.refresh(role)
    return role


#DELETE: http://localhost/roles
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 is not returning any data back to browser on deletion
async def delete_role(id: int, db: Session =Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #deleting user
    role_query = db.query(models.Roles).filter(models.Roles.id == id)
    role = role_query.first()
    
    if role == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="role with id: {id} does not exist")

    role_query.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#PUT: http://localhost/roles/1
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_role(id: int, updaterole: schemas.UpdateRole, db: Session =Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    role_query = db.query(models.Roles).filter(models.Roles.id == id)
    role = role_query.first()
    if role == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"role with id: {id} does not exist")

    role_query.update(updaterole.dict(), synchronize_session=False)
    db.commit()
    return {"data": "Successfull"}