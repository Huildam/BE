from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.region import RegionSchema
from schemas.timeline import TimelineSchema


class EventSchema(BaseModel):
    id: int
    title: str
    summary: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    view_count: int
    tags: List[str]

    # 관계된 객체들
    region: RegionSchema
    timelines: List[TimelineSchema] = []

    class Config:
        orm_mode = True

