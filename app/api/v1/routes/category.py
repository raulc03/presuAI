from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.models.category import Category
from app.schemas.category import CategoryReturn
from app.dependencies import SessionDep

from app.logging_config import logger

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
