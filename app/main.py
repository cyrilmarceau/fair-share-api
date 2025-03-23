from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
)
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlmodel import SQLModel
from fastapi import FastAPI, Request
from app.database import engine
from contextlib import asynccontextmanager
from app.auth.router import auth_router
from app.transactions.router import transaction_router


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

add_pagination(app)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


routers = [auth_router, transaction_router]

[app.include_router(router) for router in routers]
