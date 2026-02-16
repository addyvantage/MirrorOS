from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import Event
from packages.core import EventCreate


def bulk_insert_events(session: Session, events: list[EventCreate]) -> int:
    if not events:
        return 0

    orm_events: list[Event] = []
    inserted_count = 0

    for event in events:
        filters = [
            Event.connector_id == event.connector_id,
            Event.type == event.type,
            Event.timestamp == event.timestamp,
        ]
        if event.external_id is not None:
            filters.append(Event.external_id == event.external_id)
        else:
            filters.append(Event.title == event.title)

        existing_event_id = session.scalar(select(Event.id).where(and_(*filters)).limit(1))
        if existing_event_id is not None:
            continue

        orm_events.append(
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
        )
        inserted_count += 1

    # TODO: Replace this best-effort duplicate check with true upsert semantics
    # once unique constraints are finalized at the database level.
    if orm_events:
        session.add_all(orm_events)
    return inserted_count
