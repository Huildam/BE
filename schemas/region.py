from pydantic import BaseModel


class RegionResponse(BaseModel):
    id: int
    name: str
    parent_id: int

    class Config:
        orm_mode = True
