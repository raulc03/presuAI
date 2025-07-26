from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.category import Category
from app.models.user import User
from app.models.usercategory import UserCategoryLink
from app.schemas.user import UserCreate, UserReturn, UserUpdate
from app.logging_config import logger

router = APIRouter()


@router.post("/", response_model=UserReturn)
def create_user(data: UserCreate, session: SessionDep):
    new_user = User(**data.model_dump())
    links = []
    categories = session.exec(select(Category)).all()
    if len(categories) == 0:
        logger.error("Categories not found.")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Categories not found."
        )
    for category in categories:
        links.append(UserCategoryLink(category=category, user=new_user))
    try:
        session.add_all(links)
        session.commit()
        session.refresh(new_user)
        return UserReturn(**new_user.model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating the user.",
        )


@router.put("/{id}", response_model=UserReturn)
def update_user(id: int, data: UserUpdate, session: SessionDep):
    user = session.exec(select(User).where(User.id == id)).first()
    if not user:
        logger.warning(f"User with ID '{id}' not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if data.password is not None:
        user.password = data.password
    if data.balance is not None:
        user.balance = data.balance
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserReturn(**user.model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating the user.",
        )


@router.delete("/{id}")
def delete(id: int, session: SessionDep):
    user = session.exec(select(User).where(User.id == id)).first()
    if not user:
        logger.warning(f"User with ID '{id}' not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    try:
        session.delete(user)
        session.commit()
        return {"message": f"User with ID '{user.id}' deleted."}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting the user.",
        )
