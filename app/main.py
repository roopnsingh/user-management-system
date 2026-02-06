from email import message
from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1.endpoints import users

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router, prefix='/api/users', tags=[users])

@app.get("/")
def root():
    return {"message": "Hi!! Welcome to User Management System"}