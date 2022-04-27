from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database
from typing import Optional, List

router = APIRouter(
    #This is completly optional, we can use the prefix in decorator as @router.get("/userroles")
    prefix="/userroles",
    tags=['User_Roles']
)


#POST: http://localhost/userroles
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_userroles(new_role: schemas.CreateUserRoles, db: Session =Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):

    role = models.Roles(**new_role.dict())
    db.add(role)
    db.commit();
    db.refresh(role)
    return role