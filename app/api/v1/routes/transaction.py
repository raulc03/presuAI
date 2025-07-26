from fastapi import APIRouter, HTTPException, status

from app.dependencies import SessionDep
from app.models.transaction import Transaction
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
