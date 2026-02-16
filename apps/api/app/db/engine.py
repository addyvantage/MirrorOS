from pathlib import Path

from sqlalchemy import create_engine

from app.config import get_settings

settings = get_settings()


def ensure_db_dir() -> None:
    db_dir = Path(settings.db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)


ensure_db_dir()

engine = create_engine(
    settings.sqlite_url,
    connect_args={"check_same_thread": False},
    future=True,
)
