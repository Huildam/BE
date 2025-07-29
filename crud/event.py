
from sqlalchemy.orm import Session
from typing import List

from models.event import Event


def get_all_event(db: Session) -> List[Event]:
    return db.query(Event).all()


def get_event_by_id(db: Session, event_id: int) -> Event:
    return db.query(Event).filter_by(id=event_id).first()
