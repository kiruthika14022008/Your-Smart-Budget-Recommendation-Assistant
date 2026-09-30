from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    APP_NAME: str = "PocketSmart AI"

    SECRET_KEY: str = (
        "change-this-secret-key-before-production"
    )

    DATABASE_URL: str = "sqlite:///./pocketsmart.db"

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-3.8-flash"

    FRONTEND_ORIGINS: str = (
        "http://127.0.0.1:8000,"
        "http://localhost:8000"
    )

    MAX_UPLOAD_MB: int = 5

    USE_MOCK_RECOMMENDATIONS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origins(self):

        return [
            origin.strip()
            for origin in self.FRONTEND_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def gemini_enabled(self):

        return (
            bool(self.GEMINI_API_KEY)
            and not self.USE_MOCK_RECOMMENDATIONS
        )


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()