from datetime import date
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schemas.user import UserSchema


class TimelineSchema(BaseModel):
    id: int
    title: str
    summary: str
    creator: UserSchema 
    # todo: 필드 이름을 created_by로 할지 creator로 할지 결정하고
    #       변경점을 노션에 반영하기
    event_date: date
    source_name: str
    source_url: str
    source_type: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True
