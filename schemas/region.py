from typing import Optional
from pydantic import BaseModel

from schemas.base import CamelModel


class RegionResponse(BaseModel):
    id: int
    name: str
    parent: Optional['RegionResponse'] = None;


class RegionPairResponse(CamelModel):
    id: int
    name: str