from datetime import date
from datetime import datetime
from typing import Optional

from schemas.base import CamelModel
from schemas.user import UserSchema


class TimelineSchema(CamelModel):
    id: int
    title: str
    summary: str
    created_by: UserSchema
    event_date: date
    source_name: str
    source_type: str
    source_url: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    created_at: datetime


class TimelineFormSchema(CamelModel):
    user_id: int
    title: str
    summary: str
    event_date: date
