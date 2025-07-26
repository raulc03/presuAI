from decimal import Decimal
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    balance: Decimal = Decimal(0)


class UserCreate(UserBase):
    pass


class UserReturn(UserBase):
    id: int


class UserUpdate(BaseModel):
    password: str | None = None
    balance: Decimal | None = None
