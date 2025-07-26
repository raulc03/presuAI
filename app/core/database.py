from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.database_url
    else {},
    echo=settings.debug,
)


def get_session():
    with Session(engine) as session:
        yield session
