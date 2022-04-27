from __future__ import annotations #required for self referencing model should be allways first line
from array import array
from multiprocessing.dummy import Array
from sqlite3 import Timestamp
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


#pydantic -> BaseModel used for field lavel validations send from client/Browser
class clsPost(BaseModel):
    title: str
    content: str
    published: bool = True              #set default value, if user doesn't provide published becomes True by default
    rating: Optional[int] = None        #set otional parameter, if user does provide it be comes None


#________________________Lab_________________________
class lab(BaseModel):
    labname: str

class CreateLab(lab):
    pass

class LabOut(BaseModel):
    id: int
    labname: str
    labcode: str
    created_at: datetime
 
    class Config:
        orm_mode = True

#________________________________Roles________________

class CreateRole(BaseModel):
    role: str

class UpdateRole(BaseModel):
    role: str

class RoleOut(CreateRole):
    id: int

    class Config:
        orm_mode = True


#__________________________Users__________________________
class CreateSuperUser(BaseModel):
    email: EmailStr
    password: str
    role_id: int
    lab_id: int
    created_by: Optional[int]

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    role_id: int
    lab_id: int

class UpdateEmail(BaseModel):
    email: EmailStr

class UpdatePassword(BaseModel):
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    role_id: int
    created_by: Optional[int]
    role: RoleOut

    class Config:
        orm_mode = True

#________________________Authontication__________________
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class token(BaseModel):
    access_token: str
    token_type: str

class token_data(BaseModel):
    id: Optional[str] = None

#________________________User_Roles_____________________
class CreateUserRoles(BaseModel):
    user_id: int
    role_id: int

#________________________Document________________________
class Document(BaseModel):
    document_code: str
    document_name: str
    parent_id: Optional[int] = None
    valid_till_days: Optional[int] = 0
    

class CreateDocument(Document):
    srcPath: Optional[str] = None


class UpdateDocument(Document):
    srcPath: Optional[str] = None
    #document_url: Optional[str]


class DocumentOut(Document):
    id: int
    document_url: Optional[str]
    #Self referencing model
    document: Optional[List[DocumentOut]] = None 
    class Config:
        orm_mode = True







    
