from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine
from app.api.v1 import api_router as v1_router
from app.services.seeder import seed_default_categories


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_default_categories(session)

    yield


def create_app():
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.include_router(v1_router, prefix="/api/v1")

    return app


app = create_app()
