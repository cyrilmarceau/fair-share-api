from typing import Optional

import bcrypt
from sqlmodel import Session, select

from app.auth.models import User


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def get_by_email(*, db_session: Session, email: str) -> Optional[User]:
    """Returns a user object based on user email."""
    statement = select(User).where(User.email == email)
    return db_session.exec(statement).one_or_none()
