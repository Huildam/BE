from typing import Optional
from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: int
    name: str
    parent: Optional['RegionSchema'] = None;

    class Config:
        orm_mode = True
