from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MirrorOS API"
    environment: str = "development"
    log_level: str = "INFO"

    db_path: Path = Path("data/processed/mirror.db")

    model_config = SettingsConfigDict(env_prefix="MIRROR_", env_file=".env", extra="ignore")

    @property
    def sqlite_url(self) -> str:
        return f"sqlite:///{self.db_path}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
