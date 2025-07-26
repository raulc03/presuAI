from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    environment: str = "dev"
    app_name: str = "Prepai"
    debug: bool = True
    database_url: str = "sqlite:///./database.db"

    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("ENVIRONMENT") == "test" else ".env"
    )


settings = Settings()
