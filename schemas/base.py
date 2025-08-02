from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):

    class Config:
        orm_mode = True
        alias_generator = to_camel
        populate_by_name = True
