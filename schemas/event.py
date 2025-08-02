from datetime import date, datetime
from typing import List, Optional

from schemas.auth import UserResponse
from schemas.base import CamelModel
from schemas.region import RegionResponse
from schemas.timeline import TimelineResponse


class EventResponse(CamelModel):
    id: int
    title: str
    summary: str
    description: str
    region: RegionResponse
    status: str
    event_date: date
    view_count: int
    like_count: int
    tags: List[str]
    source_name: str
    source_url:  str
    source_type: str
    created_by: UserResponse
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    verified_at: Optional[datetime] = None
    timelines: List[TimelineResponse] = []


class EventCreateRequest(CamelModel):
    user_id: int
    region_id: int
    title: str
    summary: str
    description: str
    event_date: date
