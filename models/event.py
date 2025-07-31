import enum
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Enum as SAEnum
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from db.base import Base
from models.timeline import Timeline


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    # region 테이블과의 FK 관계
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    region = relationship("Region", back_populates="events")

    category = Column(String, nullable=True)

    # 상태 Enum
    status = Column(String, nullable=False, default="new")
    event_date = Column(Date, nullable=False)

    view_count = Column(Integer, nullable=False, default=0)
    like_count = Column(Integer, nullable=False, default=0)

    # PostgreSQL ARRAY로 태그 저장
    tags = Column(ARRAY(String), nullable=True, default=list)

    source_type = Column(String, nullable=False, default="")
    source_url = Column(String, nullable=False, default="")
    source_name = Column(String, nullable=False, default="")

    # 생성자(User) 테이블과의 FK 관계
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by = relationship("User", back_populates="created_events")

    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),        # INSERT 시점에 SQLAlchemy가 NOW() 호출
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),        # INSERT 시점에도 NOW()
        onupdate=func.now(),       # UPDATE 시에 NOW()로 자동 갱신
        nullable=False
    )

    is_verified = Column(Boolean, nullable=False, default=False)
    verified_at = Column(DateTime, nullable=True)
    
    region = relationship("Region")
    timelines = relationship(
        "Timeline",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by=Timeline.event_date
    )
