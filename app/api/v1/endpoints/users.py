from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserCreate, UserUpdate, UserLogin

user_router = APIRouter()

@user_router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(deps.get_db)):
    pass