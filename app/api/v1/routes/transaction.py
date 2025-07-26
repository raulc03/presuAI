from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionReturn

from app.logging_config import logger

router = APIRouter()


@router.post("/{user_id}", response_model=TransactionReturn)
def create_transaction(user_id: int, data: TransactionCreate, session: SessionDep):
    transaction = Transaction(**data.model_dump(), user_id=user_id)

    try:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return TransactionReturn(**transaction.model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating transaction.",
        )


@router.get("/{user_id}", response_model=List[Transaction])
def get_transactions(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

    try:
        transactions = session.exec(
            select(Transaction).where(Transaction.user_id == user.id)
        ).all()
        logger.debug(transactions)
        return transactions
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting the transactions for user with ID {user_id}",
        )
