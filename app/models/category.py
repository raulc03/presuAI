from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field

from app.models.usercategory import UserCategoryLink
from app.schemas.type import TypeEnum

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: TypeEnum
    name: str

    # Relationship One to Many Transaction
    transactions: list["Transaction"] = Relationship(back_populates="category")

    # Relationship Many to Many Category
    user_links: list[UserCategoryLink] = Relationship(back_populates="category")
