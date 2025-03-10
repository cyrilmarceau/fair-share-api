from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth.schemas import UserCreate, UserRegisterResponse
from app.dependencies import get_session
from app.auth.models import User

auth_router = APIRouter()


@auth_router.post("/login")
async def login():
    return {"msg": "Login route"}


@auth_router.post("/register", response_model=UserRegisterResponse)
async def register(user_in: UserCreate, db_session: Session = Depends(get_session)):
    print("Received DB session:", db_session)

    new_user = User(**user_in.model_dump())
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user
