from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import get_settings
from app.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IngestRequest(BaseModel):
    path: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest/youtube")
def ingest_youtube(_: IngestRequest) -> dict[str, str | int | bool]:
    return {
        "ok": True,
        "connector_id": "youtube_takeout_v1",
        "ingestion_run_id": str(uuid4()),
        "ingested_events": 0,
        "notes": "stub",
    }


@app.post("/ingest/twitter")
def ingest_twitter(_: IngestRequest) -> dict[str, str | int | bool]:
    return {
        "ok": True,
        "connector_id": "twitter_export_v1",
        "ingestion_run_id": str(uuid4()),
        "ingested_events": 0,
        "notes": "stub",
    }
