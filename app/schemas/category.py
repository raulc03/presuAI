from decimal import Decimal
from typing import Literal
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    type: Literal["expense", "income"]
    limit: Decimal


class CategoryCreate(CategoryBase):
    pass


class CategoryReturn(CategoryBase):
    id: int
    user_id: int


class CategoryUpdate(BaseModel):
    name: str | None = None
    limit: Decimal | None = None
