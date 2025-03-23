from datetime import datetime, timedelta, timezone
from typing import Dict
import bcrypt
import jwt
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.auth.config import AuthConfig
from app.models import TimeStampMixin


class BaseUser(SQLModel, TimeStampMixin):
    pass


class User(BaseUser, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    username: str
    password: str

    def verify_password(self, plain_password: str) -> bool:
        if not plain_password or not self.password:
            return False
        return bcrypt.checkpw(plain_password.encode("utf-8"), self.password)

    def sign_jwt(self) -> Dict[str, str]:
        auth_settings = AuthConfig()

        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        payload = {"user_id": self.id, "expires": expire.isoformat()}
        token = jwt.encode(payload, auth_settings.SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
