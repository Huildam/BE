from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base import Base


class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level = Column(Integer)
    parent_id = Column(Integer, ForeignKey("region.id"))

    parent = relationship("Region", remote_side=[id])
