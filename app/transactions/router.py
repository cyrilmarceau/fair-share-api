from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from app.auth.schemas import UserRead
from app.auth.service import get_current_user
from app.dependencies import get_session
from app.transactions.models import Transaction
from app.transactions.schemas import (
    TransactionCreate,
    TransactionCreateReponse,
    TransactionRead,
)

transaction_router = APIRouter(tags=["Transactions"])


@transaction_router.post("/transactions", response_model=TransactionCreateReponse)
async def create_transaction(
    transaction_in: TransactionCreate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db_session: Session = Depends(get_session),
):
    """Create a new transaction for the authenticated user."""
    new_transaction = Transaction(
        **transaction_in.model_dump(), user_id=current_user.id
    )

    db_session.add(new_transaction)
    db_session.commit()
    db_session.refresh(new_transaction)

    return new_transaction


@transaction_router.get("/transactions", response_model=Page[TransactionRead])
async def get_transactions(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db_session: Session = Depends(get_session),
):
    """Retrieve all transactions for the authenticated user."""
    statement = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at)
    )
    transactions = paginate(session=db_session, query=statement)

    return transactions


@transaction_router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionRead,
)
async def retrieve_transaction(
    transaction_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db_session: Session = Depends(get_session),
):
    """Retrieve a specific transaction by ID if owned by the user."""
    transaction = db_session.get(Transaction, transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_type": "resource.not_found",
                "message": f"Transaction with ID {transaction_id} does not exist or has already been deleted.",
                "loc": ["path", "transaction_id"],
            },
        )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error_type": "permission.denied",
                "message": "You don't have permission to access this transaction.",
            },
        )

    return transaction


@transaction_router.patch(
    "/transactions/{transaction_id}",
    response_model=TransactionRead,
)
async def edit_transaction(
    transaction_id: int,
    transaction_in: TransactionCreate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db_session: Session = Depends(get_session),
):
    """Update a specific transaction by ID if owned by the user."""
    transaction = db_session.get(Transaction, transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_type": "resource.not_found",
                "message": f"Transaction with ID {transaction_id} does not exist or has already been deleted.",
                "loc": ["path", "transaction_id"],
            },
        )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error_type": "permission.denied",
                "message": "You don't have permission to update this transaction.",
            },
        )

    for key, value in transaction_in.model_dump().items():
        setattr(transaction, key, value)

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    return transaction


@transaction_router.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_transaction(
    transaction_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db_session: Session = Depends(get_session),
):
    """Delete a specific transaction by ID if owned by the user."""
    transaction = db_session.get(Transaction, transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_type": "resource.not_found",
                "message": f"Transaction with ID {transaction_id} does not exist or has already been deleted.",
                "loc": ["path", "transaction_id"],
            },
        )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error_type": "permission.denied",
                "message": "You don't have permission to delete this transaction.",
            },
        )

    db_session.delete(transaction)
    db_session.commit()

    return None
