from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def safe_parse_datetime(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None

    normalized = value.strip()
    if not normalized:
        return None

    try:
        dt = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def safe_get_first_url(payload: dict[str, Any]) -> str | None:
    title_url = payload.get("titleUrl")
    if isinstance(title_url, str) and title_url.strip():
        return title_url.strip()

    details = payload.get("details")
    if isinstance(details, list):
        for item in details:
            if isinstance(item, dict):
                candidate = item.get("url")
                if isinstance(candidate, str) and candidate.strip():
                    return candidate.strip()
    return None
