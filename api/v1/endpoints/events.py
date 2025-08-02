from fastapi import APIRouter, Response
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Dict, List, Union

from db.session import get_db
from crud.event import create_event
from crud.event import get_all_event
from crud.event import get_event_by_id
from crud.timeline import create_timeline
from models.event import Event
from models.timeline import Timeline
from schemas.event import BulkEventCreateRequest, EventCreateRequest
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


@router.post("/bulk_import")
def add_event_and_timeline_from_json(
    payload: BulkEventCreateRequest, 
    db: Session = Depends(get_db)):

    saved_events: List[Event] = []
    try:
        for ev_req in payload.root:     # <-- .root 에 배열이 들어 있습니다
            # Event 생성
            ev = import_event_from_json(ev_req.model_dump(by_alias=False, exclude_unset=True))
            db.add(ev)
            db.flush()

            # Timeline 생성
            for tl_req in ev_req.timelines:
                
                tl = import_timeline_from_json(
                    tl_req.model_dump(
                        by_alias=False, 
                        exclude_unset=True),
                    ev.id
                )
                db.add(tl)

            saved_events.append(ev)

        db.commit()
        for ev in saved_events:
            db.refresh(ev)
        return saved_events

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def import_event_from_json(data: Dict) -> Event:
    """JSON 데이터로부터 Event 객체 생성"""
    # ID는 DB에서 자동 생성
    payload = EventCreateRequest.model_validate(data).model_dump()
    # 생성자 ID 고정
    payload["created_by_id"] = 1 
    return Event(**payload)


def import_timeline_from_json(data: Dict, event_id: int) -> Timeline:
    """JSON 데이터로부터 Timeline 객체 생성"""
    payload = TimelineCreateRequest.model_validate(data).model_dump()
    # 생성자 ID 고정
    payload["created_by_id"] = 1
    payload["event_id"] = event_id
    return Timeline(**payload)
