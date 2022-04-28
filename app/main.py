from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import users, auth, roles, lab, document
from .config import settings


#Now this command is not required as alembic is handling all the stuf, we can keep it as it is not breaking any of the functionality
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(lab.router)
app.include_router(document.router)



#GET: http://localhost/
@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/user")
def getuser():
    return {"message": "Hello User!"}