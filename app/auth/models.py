from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.models import TimeStampMixin


class BaseUser(SQLModel, TimeStampMixin):
    pass


class User(BaseUser, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    username: str
    password: str
