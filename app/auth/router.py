from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth.models import User
from app.auth.schemas import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRead,
    UserRegisterResponse,
)
from app.auth.service import get_by_email, get_current_user, get_password_hash
from app.dependencies import get_session


auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/login", response_model=UserLoginResponse)
async def login(user_in: UserLogin, db_session: Session = Depends(get_session)):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user and user.verify_password(user_in.password):
        return user.sign_jwt()

    raise HTTPException(
        status_code=400,
        detail={
            "error_type": "invalid.credentials",
            "message": "Incorrect email or password",
            "loc": "email",
        },
    )


@auth_router.post("/register", response_model=UserRegisterResponse)
async def register(user_in: UserCreate, db_session: Session = Depends(get_session)):
    user = get_by_email(db_session=db_session, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail={
                "error_type": "invalid.configuration",
                "message": "A user with this email already exists.",
                "loc": "email",
            },
        )

    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password

    new_user = User(**user_in.model_dump())
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user.sign_jwt()


@auth_router.get("/users/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    return current_user
