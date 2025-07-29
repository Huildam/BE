from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.event import EventDetailResponse
from crud.event import get_all_event


router = APIRouter()

@router.get("/{event_id}", response_model=List[EventDetailResponse], status_code=200)
def get_events(event_id:int, db: Session = Depends(get_db)):
    return get_all_event(db)
