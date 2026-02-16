from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID

from packages.core import EventCreate


@dataclass(frozen=True, slots=True)
class ConnectorMeta:
    connector_id: str
    source: str
    version: str
    description: str


@dataclass(slots=True)
class IngestResult:
    connector_id: str
    ingestion_run_id: UUID
    ingested_events: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    events: list[EventCreate] = field(default_factory=list)


class Connector(Protocol):
    meta: ConnectorMeta

    def ingest(self, path: str) -> IngestResult:
        ...
