from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryReturn, CategoryUpdate
from app.dependencies import SessionDep

from app.logging_config import logger

router = APIRouter()


@router.post("/{user_id}", response_model=CategoryReturn)
def create_category(user_id: int, data: CategoryCreate, session: SessionDep):
    user: User | None = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )
    category = Category(**data.model_dump(), user=user)
    try:
        session.add(category)
        session.commit()
        session.refresh(category)

        return CategoryReturn(**category.model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating the category.",
        )


@router.put("/{category_id}", response_model=CategoryReturn)
def update_category(category_id: int, data: CategoryUpdate, session: SessionDep):
    category: Category | None = session.get(Category, category_id)

    if category is None:
        logger.warning(f"Category with ID {category_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found.",
        )

    if data.name is not None:
        category.name = data.name
    if data.limit is not None:
        category.limit = data.limit

    try:
        session.add(category)
        session.commit()
        session.refresh(category)

        return CategoryReturn(**category.model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating the category",
        )


@router.delete("/{category_id}")
def delete_category(category_id: int, session: SessionDep):
    category = session.get(Category, category_id)

    if category is None:
        logger.warning(f"Category with ID {category_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found.",
        )

    try:
        session.delete(category)
        session.commit()

        return f"Category with ID {category_id} was deleted it"
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting the category.",
        )


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
