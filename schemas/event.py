from datetime import date, datetime
from typing import List, Optional

from pydantic import RootModel

from schemas.auth import UserResponse
from schemas.base import CamelModel
from schemas.region import RegionResponse
from schemas.timeline import TimelineCreateRequest, TimelineResponse


class EventResponse(CamelModel):
    id: int
    title: str
    summary: str
    description: str
    region: RegionResponse
    status: str
    event_date: date
    view_count: int
    category: str
    created_by: UserResponse
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    verified_at: Optional[datetime] = None
    timelines: List[TimelineResponse] = []


class EventCreateRequest(CamelModel):
    title: str
    summary: str
    description: Optional[str] = ""
    event_date: date
    region_id: int
    created_at: datetime
    updated_at: datetime
    view_count: int
    category: str
    status: Optional[str] = "new"
    created_by_id: Optional[int] = 1
    is_verified: Optional[bool] = False
    verified_at: Optional[datetime] = None


class EventWithTimelines(EventCreateRequest):
    timelines: List[TimelineCreateRequest]

class BulkEventCreateRequest(RootModel[List[EventWithTimelines]]):
    pass