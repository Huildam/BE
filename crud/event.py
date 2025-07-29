
from sqlalchemy.orm import Session
from typing import List

from models.event import Event


def get_all_event(db: Session) -> List[Event]:
    return db.query(Event).all()