from fastapi import APIRouter
from app.api.v1.routes.users import router as user_router
from app.api.v1.routes.category import router as category_router
from app.api.v1.routes.transaction import router as transaction_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(category_router, prefix="/categories", tags=["Category"])
api_router.include_router(
    transaction_router, prefix="/transaction", tags=["Transaction"]
)
