from sqlmodel import SQLModel
from fastapi import FastAPI
from app.database import engine
from contextlib import asynccontextmanager
from app.auth.router import auth_router


@asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    print("sub startup")
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully")
        yield
    finally:
        print("finally")
        print("sub shutdown")


app = FastAPI(
    title="Fair-share API",
    version="0.0.1",
    debug=True,
    docs_url=None,
    redoc_url="/docs",
    lifespan=lifespan_wrapper,
)

app.include_router(auth_router)
