from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import text
from sqlalchemy.orm import relationship

from db.base import Base  # declarative_base()를 정의한 모듈에서 import


class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(BigInteger, primary_key=True)
    event_id = Column(BigInteger, ForeignKey("event.id"), nullable=False)
    title = Column(String(255), nullable=False)
    region_name = Column(String(100), nullable=True)
    summary = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    source_name = Column(String(255), nullable=False)
    source_url = Column(String(500), nullable=True)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=True)
    source_type = Column(
        String(20),
        nullable=False,
    )
    created_by = Column(BigInteger, ForeignKey("user.id"), nullable=True)
    is_verified = Column(Boolean, server_default=text("FALSE"), nullable=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    is_active = Column(Boolean, server_default=text("TRUE"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "source_type IN ('news','user')", name="ck_timeline_source_type"
        ),
    )

    # 관계 설정
    event = relationship("Event", back_populates="timeline_items")
    region = relationship("Region")
    creator = relationship("User")
