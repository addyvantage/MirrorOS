from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import get_settings
from app.db.session import SessionLocal
from app.logging import configure_logging
from app.repositories import bulk_insert_events
from packages.connectors import YouTubeTakeoutConnector

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
def ingest_youtube(request: IngestRequest) -> dict[str, str | int | bool | list[str]]:
    connector = YouTubeTakeoutConnector()
    result = connector.ingest(request.path)

    inserted_events = 0
    if result.events:
        with SessionLocal() as session:
            try:
                inserted_events = bulk_insert_events(session, result.events)
                session.commit()
            except Exception as exc:  # pragma: no cover - best effort error propagation
                session.rollback()
                result.errors.append(f"Failed to persist ingested events: {exc}")

    return {
        "ok": len(result.errors) == 0,
        "connector_id": result.connector_id,
        "ingestion_run_id": str(result.ingestion_run_id),
        "ingested_events": inserted_events,
        "warnings": result.warnings,
        "errors": result.errors,
    }


@app.post("/ingest/twitter")
def ingest_twitter(_: IngestRequest) -> dict[str, str | int | bool | list[str]]:
    return {
        "ok": True,
        "connector_id": "twitter_export_v1",
        "ingestion_run_id": str(uuid4()),
        "ingested_events": 0,
        "warnings": [],
        "errors": [],
    }
