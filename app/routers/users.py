from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    #This is completly optional, we can use the prefix in decorator as @router.get("/users")
    prefix="/users",
    tags=['Users']
)

#GET: http://localhost/users
@router.get("/", response_model=List[schemas.UserOut])
async def root(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    users = db.query(models.Users).all() 
    print(users)
    return users

#GET: http://localhost/users/1
@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #imported Response, Status, HTTPException from FastAPI
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not found")
    return user


#POST: http://localhost/users/createsuperadmin 
@router.post("/createsuperadmin", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateSuperUser, db: Session =Depends(get_db)):
    print(user)
    #hash the password  - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit();
    db.refresh(new_user)
    return new_user


#POST: http://localhost/users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(created_by=current_user.id, **user.dict())
    #new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit();
    db.refresh(new_user)
    return new_user


#DELETE: http://localhost/users
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 is not returning any data back to browser on deletion
async def delete_user(id: int, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #deleting user
    user_query = db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not exist")

    #if user.created_by != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                        detail="You are not authorize to perform requested opration")

    user_query.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#PUT: http://localhost/users/1
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user_email(id: int, updateUser: schemas.UpdateEmail, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not exist")

    user_query.update(updateUser.dict(), synchronize_session=False)
    db.commit()
    return {"data": "Successfull"}
