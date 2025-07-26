from typing import Literal
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    type: Literal["expense", "income"]


class CategoryReturn(CategoryBase):
    id: int
