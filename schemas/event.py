from datetime import date, datetime
from typing import List, Optional

from schemas.base import CamelModel
from schemas.region import RegionSchema
from schemas.timeline import TimelineSchema
from schemas.user import UserSchema


class EventSchema(CamelModel):
    id: int
    title: str
    summary: str
    description: str
    region: RegionSchema
    status: str
    event_date: date
    view_count: int
    like_count: int
    tags: List[str]
    source_name: str
    source_url:  str
    source_type: str
    created_by: UserSchema
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    verified_at: Optional[datetime] = None
    timelines: List[TimelineSchema] = []


class EventFormSchema(CamelModel):
    user_id: int
    region_id: int
    title: str
    summary: str
    description: str
    event_date: date
