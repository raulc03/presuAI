from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    balance: Decimal = Field(default=0, decimal_places=2)

    # Relationship
    categories: list["Category"] = Relationship(back_populates="user")  # noqa: F821
    transactions: list["Transaction"] = Relationship(back_populates="user")
