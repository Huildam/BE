from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.event import EventDetailResponse
from crud.event import get_all_event
from crud.event import get_event_by_id


router = APIRouter()

@router.get("/", response_model=List[EventDetailResponse], status_code=200)
def get_total_event(db: Session = Depends(get_db)):
    return get_all_event(db)


@router.get("/{event_id}", response_model=EventDetailResponse, status_code=200)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    return get_event_by_id(db,event_id)
