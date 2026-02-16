from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from uuid import UUID, uuid4

from packages.connectors.base import ConnectorMeta, IngestResult
from packages.core import EventCreate, dedupe_events, safe_get_first_url, safe_parse_datetime


class YouTubeTakeoutConnector:
    meta = ConnectorMeta(
        connector_id="youtube_takeout_v1",
        source="youtube",
        version="1.0.0",
        description="Ingests YouTube Google Takeout watch/search history JSON exports.",
    )

    def __init__(self, ingestion_run_id: UUID | None = None):
        self._ingestion_run_id = ingestion_run_id or uuid4()

    def ingest(self, path: str) -> IngestResult:
        root = Path(path).expanduser()
        warnings: list[str] = []
        errors: list[str] = []
        events: list[EventCreate] = []

        if not root.exists():
            errors.append(f"Takeout path does not exist: {root}")
            return IngestResult(
                connector_id=self.meta.connector_id,
                ingestion_run_id=self._ingestion_run_id,
                ingested_events=0,
                warnings=warnings,
                errors=errors,
                events=[],
            )

        discovered = self._discover_history_files(root)
        watch_paths = discovered["watch"]
        search_paths = discovered["search"]

        if not watch_paths:
            warnings.append("watch-history.json not found in provided Takeout path.")
        if not search_paths:
            warnings.append("search-history.json not found in provided Takeout path.")

        for file_path in watch_paths:
            records = self._load_json_records(file_path, errors)
            for index, record in enumerate(records):
                if not isinstance(record, dict):
                    warnings.append(f"{file_path}: record {index} is not an object; skipped.")
                    continue
                event = self._build_watch_event(record, file_path, index, warnings)
                if event:
                    events.append(event)

        for file_path in search_paths:
            records = self._load_json_records(file_path, errors)
            for index, record in enumerate(records):
                if not isinstance(record, dict):
                    warnings.append(f"{file_path}: record {index} is not an object; skipped.")
                    continue
                event = self._build_search_event(record, file_path, index, warnings)
                if event:
                    events.append(event)

        deduped_events, duplicates = dedupe_events(events)
        if duplicates:
            warnings.append(f"Skipped {duplicates} duplicate event(s) by external_id/timestamp/type.")

        return IngestResult(
            connector_id=self.meta.connector_id,
            ingestion_run_id=self._ingestion_run_id,
            ingested_events=len(deduped_events),
            warnings=warnings,
            errors=errors,
            events=deduped_events,
        )

    def _discover_history_files(self, root: Path) -> dict[str, list[Path]]:
        found: dict[str, list[Path]] = {"watch": [], "search": []}
        targets = {
            "watch-history.json": "watch",
            "search-history.json": "search",
        }

        if root.is_file():
            key = targets.get(root.name.lower())
            if key:
                found[key].append(root)
            return found

        for candidate in root.rglob("*.json"):
            key = targets.get(candidate.name.lower())
            if key:
                found[key].append(candidate)

        for key in found:
            found[key] = sorted(found[key])

        return found

    def _load_json_records(self, path: Path, errors: list[str]) -> list[object]:
        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError:
            errors.append(f"Missing expected file: {path}")
            return []
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {path}: {exc}")
            return []
        except OSError as exc:
            errors.append(f"Failed reading {path}: {exc}")
            return []

        if not isinstance(payload, list):
            errors.append(f"Expected JSON array in {path}, got {type(payload).__name__}.")
            return []
        return payload

    def _build_watch_event(
        self,
        record: dict[str, object],
        file_path: Path,
        index: int,
        warnings: list[str],
    ) -> EventCreate | None:
        timestamp = safe_parse_datetime(record.get("time") if isinstance(record.get("time"), str) else None)
        if timestamp is None:
            warnings.append(f"{file_path}: watch record {index} missing/invalid time; skipped.")
            return None

        title = record.get("title")
        normalized_title = title.strip() if isinstance(title, str) and title.strip() else "Untitled YouTube watch"

        url = safe_get_first_url(record)
        external_id = self._extract_video_id(url)
        creator = self._extract_creator(record)

        return EventCreate(
            source=self.meta.source,
            domain="video",
            type="watched",
            external_id=external_id,
            connector_id=self.meta.connector_id,
            ingestion_run_id=self._ingestion_run_id,
            title=normalized_title,
            creator=creator,
            url=url,
            timestamp=timestamp,
            duration_seconds=None,
            raw_metadata=record,
        )

    def _build_search_event(
        self,
        record: dict[str, object],
        file_path: Path,
        index: int,
        warnings: list[str],
    ) -> EventCreate | None:
        timestamp = safe_parse_datetime(record.get("time") if isinstance(record.get("time"), str) else None)
        if timestamp is None:
            warnings.append(f"{file_path}: search record {index} missing/invalid time; skipped.")
            return None

        title = record.get("title")
        normalized_title = title.strip() if isinstance(title, str) and title.strip() else "YouTube search"
        url = safe_get_first_url(record)

        return EventCreate(
            source=self.meta.source,
            domain="search",
            type="searched",
            external_id=None,
            connector_id=self.meta.connector_id,
            ingestion_run_id=self._ingestion_run_id,
            title=normalized_title,
            creator=None,
            url=url,
            timestamp=timestamp,
            duration_seconds=None,
            raw_metadata=record,
        )

    def _extract_creator(self, record: dict[str, object]) -> str | None:
        subtitles = record.get("subtitles")
        if not isinstance(subtitles, list):
            return None

        for subtitle in subtitles:
            if isinstance(subtitle, dict):
                name = subtitle.get("name")
                if isinstance(name, str) and name.strip():
                    return name.strip()
        return None

    def _extract_video_id(self, url: str | None) -> str | None:
        if not url:
            return None
        try:
            parsed = urlparse(url)
        except ValueError:
            return None

        host = parsed.netloc.lower()
        if host.endswith("youtube.com"):
            video_ids = parse_qs(parsed.query).get("v")
            if video_ids and video_ids[0]:
                return video_ids[0]
        if host == "youtu.be":
            short_id = parsed.path.strip("/").split("/", 1)[0]
            return short_id or None
        return None
