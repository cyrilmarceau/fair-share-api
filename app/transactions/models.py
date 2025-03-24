import datetime
import enum
from typing import Optional
from sqlmodel import Column, Enum, Field, Relationship, SQLModel


from app.auth.models import User
from app.models import TimeStampMixin


class TransactionDirection(str, enum.Enum):
    TO_PAY = "to_pay"
    TO_RECEIVE = "to_receive"


class BaseTransaction(SQLModel, TimeStampMixin):

    pass


class Transaction(BaseTransaction, table=True):
    id: int = Field(
        primary_key=True, description="Unique ID that represent an transaction"
    )
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship()
    to: str = Field(max_length=60, description="User who's need to pay or receive")
    direction: TransactionDirection = Field(
        default=TransactionDirection.TO_PAY,
        sa_column=Column(Enum(TransactionDirection)),
        description="Direction of the transaction (to pay or to receive)",
    )
    amount: float = Field(
        gt=0,
        description="Amount of the transaction, must be greater than 0",
    )
    title: str = Field(
        max_length=255,
        description="Title of the transaction, maximum length of 255 characters",
    )
    category: str = Field(
        max_length=255,
        description="Category of the transaction, maximum length of 255 characters",
    )
    due_date: datetime.datetime = Field(
        description="Date where the transaction is due",
    )
