from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserCreate, UserUpdate, UserLogin
from app.services import user as user_services
from app.core import security
user_router = APIRouter()

@user_router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = user_services.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email Already Exists!!")
    
    db_user = user_services.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username Already Exits!!")

    return user_services.create_user(db, user)

@user_router.put("/user_update/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    db_user = user_services.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found!!")
    return db_user


@user_router.post("/login", response_model=User, status_code=status.HTTP_201_CREATED)
def login(user: UserLogin, db: Session = Depends(deps.get_db)):
    pass

@user_router.delete("delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    success = user_services.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@user_router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    return current_user

@user_router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    users = user_services.get_users(db, skip=skip, limit=limit)
    return users

@user_router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_user = user_services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
