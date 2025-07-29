from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.region import RegionResponse
from schemas.timeline import TimelineItemResponse


class EventDetailResponse(BaseModel):
    id: int
    title: str
    summary: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    view_count: int

    # 관계된 객체들
    region: RegionResponse
    timeline_items: List[TimelineItemResponse] = []

    class Config:
        orm_mode = True
