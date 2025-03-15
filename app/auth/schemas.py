from typing import Optional
from pydantic import BaseModel, field_validator
from pydantic.networks import EmailStr
from sqlmodel import Field

from app.models import DispatchBase, TimeStampMixin


class AccessToken(DispatchBase):
    access_token: Optional[str] = Field(None, nullable=True)


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


class UserRegisterResponse(AccessToken):
    pass


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


class UserLoginResponse(AccessToken):
    pass


class UserRead(TimeStampMixin, UserBase):
    id: int = Field(primary_key=True)
