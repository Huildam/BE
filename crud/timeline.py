
from db import session
from models.timeline import Timeline
from schemas.timeline import TimelineCreateRequest


def create_timeline(db: session, event_id: int, timeline_form: TimelineCreateRequest) -> Timeline:
    data = timeline_form.model_dump()
    if "user_id" in data:
        data["created_by_id"] = data.pop("user_id")
    data["event_id"] = event_id
    db_timeline = Timeline(**data)

    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline