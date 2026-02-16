from collections import defaultdict
from datetime import timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Event


def get_recent_recommendations(session: Session, limit: int = 10) -> list[dict[str, Any]]:
    recent_events = list(
        session.scalars(
            select(Event)
            .where(Event.domain == "video")
            .order_by(Event.timestamp.desc())
            .limit(50)
        )
    )
    if not recent_events:
        return []

    events_by_creator: dict[str, list[Event]] = defaultdict(list)
    for event in recent_events:
        creator = event.creator.strip() if event.creator and event.creator.strip() else "Unknown creator"
        events_by_creator[creator].append(event)

    max_count = max(len(events) for events in events_by_creator.values())
    recommendations: list[dict[str, Any]] = []

    for creator, creator_events in events_by_creator.items():
        creator_events.sort(key=lambda event: event.timestamp, reverse=True)
        most_recent = creator_events[0]
        deduped_receipts: list[dict[str, str]] = []
        seen_receipt_keys: set[tuple[str, str, str]] = set()

        for event in creator_events:
            normalized_timestamp = (
                event.timestamp.astimezone(timezone.utc)
                if event.timestamp.tzinfo is not None
                else event.timestamp.replace(tzinfo=timezone.utc)
            )
            timestamp_key = normalized_timestamp.isoformat()
            dedupe_id = event.external_id if event.external_id else event.title
            receipt_key = (dedupe_id, timestamp_key, event.type)
            if receipt_key in seen_receipt_keys:
                continue
            seen_receipt_keys.add(receipt_key)
            deduped_receipts.append(
                {
                    "event_id": str(event.id),
                    "title": event.title,
                    "timestamp": timestamp_key,
                    "connector_id": event.connector_id,
                }
            )

        recommendations.append(
            {
                "title": most_recent.title,
                "creator": creator,
                "url": most_recent.url or "",
                "score": len(creator_events) / max_count,
                "receipts": deduped_receipts,
                "_most_recent_timestamp": most_recent.timestamp,
            }
        )

    recommendations.sort(
        key=lambda recommendation: (
            recommendation["score"],
            recommendation["_most_recent_timestamp"],
        ),
        reverse=True,
    )

    for recommendation in recommendations:
        recommendation.pop("_most_recent_timestamp", None)

    return recommendations[:limit]
