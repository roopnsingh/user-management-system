import token
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    first_name: str
    last_name: str
    password: SecretStr = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> SecretStr:
        pwd = value.get_secret_value()

        if not re.search(r"[A-Z]", pwd):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", pwd):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", pwd):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            raise ValueError("Password must contain at least one special character")

        return value


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[SecretStr] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Optional[SecretStr]) -> Optional[SecretStr]:
        if value is None:
            return value

        pwd = value.get_secret_value()

        if not re.search(r"[A-Z]", pwd):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", pwd):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", pwd):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            raise ValueError("Password must contain at least one special character")

        return value

class User(BaseModel):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

class Token(BaseModel):
    access_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: int
    exp: int
    type: str