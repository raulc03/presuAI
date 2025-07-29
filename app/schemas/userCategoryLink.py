from decimal import Decimal
from pydantic import BaseModel, Field

from app.schemas.category import CategoryReturn


class UserCategoryBase(BaseModel):
    limit: Decimal = Field(default=Decimal(0), max_digits=8, decimal_places=2)


class UserCategoryCreate(UserCategoryBase):
    pass


class UserCategoryUpdate(BaseModel):
    limit: Decimal | None = None


class UserCategoryReturn(UserCategoryBase):
    category: CategoryReturn
    limit: Decimal = Field(default=Decimal(0), max_digits=8, decimal_places=2)
