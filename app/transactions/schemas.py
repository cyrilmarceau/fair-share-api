import datetime
from typing import Optional

from app.auth.schemas import UserRead
from app.models import DispatchBase
from app.transactions.models import TransactionDirection


class TransactionBase(DispatchBase):
    to: str
    direction: TransactionDirection = TransactionDirection.TO_PAY
    amount: float
    title: str
    category: str
    due_date: datetime.datetime

    class Config:
        json_schema_extra = {
            "example": {
                "to": "John doe",
                "direction": "to_pay",
                "amount": 42.50,
                "motif": "Grocery shopping",
            }
        }


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionRead):
    pass


class TransactionCreateReponse(TransactionResponse):
    user: UserRead
