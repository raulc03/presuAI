from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.models.category import Category
from app.models.user import User
from app.models.usercategory import UserCategoryLink
from app.schemas.category import CategoryReturn
from app.dependencies import SessionDep

from app.logging_config import logger
from app.schemas.userCategoryLink import UserCategoryReturn, UserCategoryUpdate

router = APIRouter()


@router.get("/", response_model=List[CategoryReturn])
def get_all_categories(session: SessionDep):
    try:
        categories = session.exec(select(Category)).all()
        return categories
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting categories",
        )


@router.get("/{user_id}", response_model=List[UserCategoryReturn])
def get_categories_by_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    try:
        userCategories = session.exec(
            select(UserCategoryLink).where(UserCategoryLink.user == user)
        ).all()
        return userCategories
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting categories by user",
        )


@router.put("/{user_id}/{category_id}", response_model=UserCategoryReturn)
def update_category_limit(
    user_id: int, category_id: int, data: UserCategoryUpdate, session: SessionDep
):
    user = session.get(User, user_id)
    category = session.get(Category, category_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found",
        )

    try:
        userCategory = session.exec(
            select(UserCategoryLink).where(
                UserCategoryLink.user == user, UserCategoryLink.category == category
            )
        ).first()
        if userCategory is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no category to update",
            )
        if data.limit is not None:
            userCategory.limit = data.limit

        session.add(userCategory)
        session.commit()
        session.refresh(userCategory)
        session.refresh(category)
        return UserCategoryReturn(
            **userCategory.model_dump(),
            category=CategoryReturn(**category.model_dump()),
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating the limit",
        )
