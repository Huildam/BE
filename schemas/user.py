from schemas.base import CamelModel


class UserSchema(CamelModel):
    id: int
    username: str
