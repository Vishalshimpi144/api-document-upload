from email.policy import default
from enum import unique
from multiprocessing.dummy import Array
from unittest.mock import DEFAULT
from xmlrpc.client import DateTime
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null
from sqlalchemy.orm import relationship

class Lab(Base):
    __tablename__ = "lab"

    id =Column(Integer, primary_key=True, nullable=False)
    labname = Column(String, nullable=False)
    labcode = Column(String)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))

class Roles(Base):
    __tablename__ ="roles"

    id = Column(Integer, primary_key=True, nullable=False)
    role = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))

class Users(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", 
                        ondelete="SET DEFAULT"), nullable=False)
    lab_id = Column(Integer, ForeignKey("lab.id", 
                        ondelete="SET DEFAULT"), nullable=True)
    phone_number = Column(String)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET DEFAULT"))
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
        
    role = relationship("Roles") #refering to the class not table name
    lab = relationship("Lab")

class User_Roles(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True, nullable=False)
    document_code = Column(String, unique=True)
    document_name = Column(String, nullable=False)
    document_url = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("document.id", ondelete="CASCADE"))
    valid_till_days = Column(Integer)
    s3_document_name = Column(String)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET DEFAULT"))
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET DEFAULT"))
    updated_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
                
    document = relationship("Document")


