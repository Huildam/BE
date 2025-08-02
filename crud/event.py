
from sqlalchemy.orm import Session
from typing import List

from models.event import Event
from schemas.event import EventCreateRequest


def get_all_event(db: Session, query_parameter: dict) -> List[Event]:
    category = query_parameter.get("category")
    region_id = query_parameter.get("region_id")
    query = db.query(Event)
    if category:
        query = query.filter(Event.category == category)
    if region_id:
        query = query.filter(Event.region_id == region_id)
    return query.all()


def get_event_by_id(db: Session, event_id: int) -> Event:
    return db.query(Event).filter_by(id=event_id).first()


def create_event(db: Session, event_form: EventCreateRequest) -> Event:
    data = event_form.model_dump()
    if "user_id" in data:
        data["created_by_id"] = data.pop("user_id")
    db_event = Event(**data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event