from datetime import date, datetime
from typing import List, Optional

from schemas.base import CamelModel
from schemas.region import RegionSchema
from schemas.timeline import TimelineSchema


class EventSchema(CamelModel):
    id: int
    title: str
    summary: str
    event_date: date
    created_at: datetime
    updated_at: datetime
    view_count: int
    tags: List[str]
    source_name: str
    source_url:  str
    source_type: str

    # 관계된 객체들
    region: RegionSchema
    timelines: List[TimelineSchema] = []

    class Config:
        orm_mode = True


class EventFormSchema(CamelModel):
    user_id: int
    region_id: int
    title: str
    summary: str
    description: str
    event_date: date
