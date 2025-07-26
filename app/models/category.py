from decimal import Decimal
from sqlmodel import Relationship, SQLModel, Field

from app.models.user import User
from app.schemas.type import TypeEnum


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: TypeEnum
    name: str
    limit: Decimal = Field(decimal_places=2)

    # Relationship
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="categories")

    transactions: list["Transaction"] = Relationship(back_populates="category")
