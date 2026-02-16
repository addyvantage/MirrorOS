from sqlalchemy.orm import Session

from app.models import Event
from packages.core import EventCreate


def bulk_insert_events(session: Session, events: list[EventCreate]) -> int:
    if not events:
        return 0

    orm_events = [
        Event(
            source=event.source,
            domain=event.domain,
            type=event.type,
            external_id=event.external_id,
            connector_id=event.connector_id,
            ingestion_run_id=event.ingestion_run_id,
            title=event.title,
            creator=event.creator,
            url=event.url,
            timestamp=event.timestamp,
            duration_seconds=event.duration_seconds,
            raw_metadata=event.raw_metadata,
        )
        for event in events
    ]

    # TODO: Add idempotent upsert semantics once unique constraints are finalized.
    session.add_all(orm_events)
    return len(orm_events)
