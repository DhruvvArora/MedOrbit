from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BACKEND_DIR / ".env"
DEFAULT_SQLITE_PATH = (BACKEND_DIR / "medorbit.db").resolve()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_NAME: str = "MedOrbit"
    DEBUG: bool = False

    DATABASE_URL: str = f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"

    SECRET_KEY: str = "medorbit-hackathon-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    SKIP_AUTH: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()