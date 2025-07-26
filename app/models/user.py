from decimal import Decimal
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from app.models.usercategory import UserCategoryLink

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    balance: Decimal = Field(default=0, decimal_places=2)

    # Relationship One to Many Transaction
    transactions: list["Transaction"] = Relationship(back_populates="user")

    # Relationship Many to Many Category
    category_links: list[UserCategoryLink] = Relationship(
        back_populates="user",
        cascade_delete=True,
    )
