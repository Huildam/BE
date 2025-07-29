from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import text
from sqlalchemy.orm import relationship

from db.base import Base  # declarative_base()를 정의한 모듈에서 import


class Event(Base):
    __tablename__ = "event"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255), nullable=False)
    region_name = Column(String(100), nullable=True)
    summary = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=True)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    is_active = Column(Boolean, server_default=text("TRUE"), nullable=False)
    view_count = Column(Integer, server_default=text("0"), nullable=False)

    # 관계 설정
    region = relationship("Region", back_populates="event")
    timeline_items = relationship(
        "Timeline",
        back_populates="event",
        cascade="all, delete-orphan",
    )
