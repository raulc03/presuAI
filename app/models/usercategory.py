from decimal import Decimal
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category


class UserCategoryLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    category_id: int | None = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
    limit: Decimal = Field(default=0, max_digits=8, decimal_places=2)

    # Relationship
    user: "User" = Relationship(back_populates="category_links")
    category: "Category" = Relationship(back_populates="user_links")
