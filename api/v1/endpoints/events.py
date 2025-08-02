from fastapi import APIRouter, Response
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Union

from db.session import get_db
from crud.event import create_event, find_event
from crud.event import get_all_event
from crud.event import get_event_by_id
from crud.timeline import create_timeline
from schemas.event import EventCreateRequest
from schemas.event import EventResponse
from schemas.timeline import TimelineResponse
from schemas.timeline import TimelineCreateRequest


router = APIRouter()


@router.get("", response_model=List[EventResponse], status_code=200)
def get_total_event(db: Session = Depends(get_db)):
    return get_all_event(db)


@router.get("/{event_id}", response_model=EventResponse, status_code=200)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    return get_event_by_id(db, event_id)


@router.post("", response_model=EventResponse, status_code=201)
def add_event(event_form: EventCreateRequest, db: Session = Depends(get_db)):
    event = create_event(db, event_form)
    if not event:
        raise HTTPException(status_code=400, detail="Event was not created.")
    return event


@router.post("/{event_id}/timelines", response_model=TimelineResponse, status_code=201)
def add_timeline(event_id: int, timeline_form: TimelineCreateRequest, db: Session = Depends(get_db)):
    timeline = create_timeline(db, event_id, timeline_form)
    if not timeline:
        raise HTTPException(status_code=400, detail="Timeline was not created.")
    return timeline