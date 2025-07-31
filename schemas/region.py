from typing import Optional
from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: int
    name: str
    parent: Optional['RegionSchema'] = None;
