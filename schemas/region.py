from typing import Optional
from pydantic import BaseModel


class RegionResponse(BaseModel):
    id: int
    name: str
    parent: Optional['RegionResponse'] = None;

    class Config:
        orm_mode = True
