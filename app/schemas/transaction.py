from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime


class Transaction(BaseModel):
    amount: Decimal = Field(max_digits=8, decimal_places=2, ge=0)
    txn_datetime: datetime
    type: Literal["expense", "income"]
    # TODO: Crear variables globales para valores como max_length
    description: str = Field(max_length=60)


class TransactionReturn(Transaction):
    id: int
    user_id: int
    category_id: int | None = Field(default=None)
    description: str


class TransactionCreate(Transaction):
    pass


class TransactionUpdate(BaseModel):
    amount: Decimal | None = None
    txn_datetime: datetime | None = None
    type: Literal["expense", "income"] | None = None
    category_id: int | None = None
    description: str | None = Field(default=None, max_length=60)
