from decimal import Decimal
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    pass


class UserReturn(UserBase):
    id: int


class UserUpdate(BaseModel):
    password: str | None = None
