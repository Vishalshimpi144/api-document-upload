from msilib import schema
from xml.dom import expatbuilder
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#SECRETE_KEY
#ALGORITHM
#EXPIRATION_TIME

SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data= dict):
    to_encode = data.copy()
    
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.token_data(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate the credentials", headers={"WWW-Authonticate": "bearer"})
    
    #fetch the user details from database everytime
    access_token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == access_token.id).first()
    return user
    #return verify_access_token(token, credentials_exception)