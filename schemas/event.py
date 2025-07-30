from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from pydantic.alias_generators import to_snake

from schemas.region import RegionSchema
from schemas.timeline import TimelineSchema


class EventSchema(BaseModel):
    id: int
    title: str
    summary: str
    event_date: date
    created_at: datetime
    updated_at: datetime
    view_count: int
    tags: List[str]

    # 관계된 객체들
    region: RegionSchema
    timelines: List[TimelineSchema] = []

    class Config:
        orm_mode = True


class EventFormSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    user_id: int
    region_id: int
    title: str
    summary: str
    description: str
    event_date: date
