from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status

import bcrypt
import jwt
from sqlmodel import Session, select

from app.auth.models import User
from app.auth.config import AuthConfig, oauth2_scheme
from app.dependencies import get_session


async def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


async def get_by_email(*, db_session: Session, email: str) -> Optional[User]:
    """Returns a user object based on user email."""
    statement = select(User).where(User.email == email)
    return db_session.exec(statement).one_or_none()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    auth_settings = AuthConfig()

    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db_session.get(User, user_id)

    if user is None:
        raise credentials_exception

    return user
