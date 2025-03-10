from typing import Optional
from pydantic import BaseModel, field_validator
from pydantic.networks import EmailStr
from sqlmodel import Field

from app.models import DispatchBase


class UserBase(BaseModel):
    username: str
    email: EmailStr

    @field_validator("email")
    def email_must_be_valid(cls, email):
        if not email:
            raise ValueError("Email is required")
        return email


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def password_must_be_valid(cls, password):
        if not password:
            raise ValueError("Password is required")
        return password


class UserRegisterResponse(DispatchBase):
    token: Optional[str] = Field(None, nullable=True)
