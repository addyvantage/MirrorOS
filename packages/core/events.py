from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(slots=True)
class EventCreate:
    source: str
    domain: str
    type: str
    external_id: str | None
    connector_id: str
    ingestion_run_id: UUID
    title: str
    creator: str | None
    url: str | None
    timestamp: datetime
    duration_seconds: int | None
    raw_metadata: dict[str, Any]


def dedupe_events(events: list[EventCreate]) -> tuple[list[EventCreate], int]:
    """De-dupe events by (external_id, timestamp, type) when external_id exists."""
    unique_events: list[EventCreate] = []
    seen: set[tuple[str, str, str]] = set()
    duplicates = 0

    for event in events:
        if event.external_id:
            key = (event.external_id, event.timestamp.isoformat(), event.type)
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
        unique_events.append(event)

    return unique_events, duplicates
