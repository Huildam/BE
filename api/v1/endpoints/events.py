from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from crud.event import create_event
from crud.event import get_all_event
from crud.event import get_event_by_id
from schemas.event import EventFormSchema
from schemas.event import EventSchema


router = APIRouter()

@router.get("/", response_model=List[EventSchema], status_code=200)
def get_total_event(db: Session = Depends(get_db)):
    return get_all_event(db)


@router.get("/{event_id}", response_model=EventSchema, status_code=200)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    return get_event_by_id(db,event_id)


@router.post("", response_model=EventSchema, status_code=201)
def add_event(event_form: EventFormSchema, db: Session = Depends(get_db)):
    event = create_event(db, event_form)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
