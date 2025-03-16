from datetime import datetime, timezone
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status

import bcrypt
import jwt
from sqlmodel import Session, select

from app.auth.models import User
from app.auth.config import AuthConfig, oauth2_scheme
from app.dependencies import get_session


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def get_by_email(*, db_session: Session, email: str) -> Optional[User]:
    """Returns a user object based on user email."""
    statement = select(User).where(User.email == email)
    return db_session.exec(statement).one_or_none()


def get_current_user(
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
        expires = payload.get("expires")

        if user_id is None:
            raise credentials_exception

        # Vérifier si le token a expiré
        expire_time = datetime.fromisoformat(expires)
        if datetime.now(timezone.utc) > expire_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception

    user = db_session.get(User, user_id)

    if user is None:
        raise credentials_exception

    return user
