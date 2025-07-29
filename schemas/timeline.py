from datetime import datetime
from pydantic import BaseModel


class TimelineItemResponse(BaseModel):
    id: int
    title: str
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True
