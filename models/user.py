from datetime import datetime
from datetime import timezone

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    accumulated_rewards = Column(Integer)
    can_withdraw = Column(Boolean)
    region_id = Column(Integer, ForeignKey("region.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    region = relationship("Region")
    created_events = relationship("Event", back_populates="created_by")

