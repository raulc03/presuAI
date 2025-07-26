from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from app.models.category import Category
from app.models.user import User
from app.schemas.type import TypeEnum


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: Decimal = Field(max_digits=8, decimal_places=2, ge=0)
    txn_datetime: datetime
    type: TypeEnum | None = Field(default=None)
    description: str = Field(max_length=60)

    # Relationship
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="transactions")

    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Category | None = Relationship(back_populates="transactions")
