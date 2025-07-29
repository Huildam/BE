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

from db.base import Base  # declarative_base()를 정의한 모듈에서 import


class StatusEnum(enum.Enum):
    pending = "pending"  # 등록 대기중
    new = "new"  # 새로 등록됨
    progress = "progress"  # 진행중
    done = "done"  # 종결됨


class SourceTypeEnum(enum.Enum):
    news = "news"  # 기사
    official = "official"  # 공공기관
    user = "user"  # 일반인 제보


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    # region 테이블과의 FK 관계
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    region = relationship("Region", back_populates="events")

    category = Column(String, nullable=False)

    # 상태 Enum
    status = Column(
        SAEnum(StatusEnum, name="event_status"), nullable=False, default=StatusEnum.new
    )

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    view_count = Column(Integer, nullable=False, default=0)
    like_count = Column(Integer, nullable=False, default=0)

    # PostgreSQL ARRAY로 태그 저장
    tags = Column(ARRAY(String), nullable=False, default=list)

    source_type = Column(SAEnum(SourceTypeEnum, name="source_type"), nullable=False)
    source_url = Column(String, nullable=False)
    source_name = Column(String, nullable=False)

    # 생성자(User) 테이블과의 FK 관계
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by = relationship("User", back_populates="created_events")

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    is_verified = Column(Boolean, nullable=False, default=False)
    verified_at = Column(DateTime, nullable=True)
    
    region = relationship("Region")
    timelines = relationship(
        "Timeline",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    # id = Column(BigInteger, primary_key=True)
    # title = Column(String(255), nullable=False)
    # region_name = Column(String(100), nullable=True)
    # summary = Column(Text, nullable=False)
    # event_date = Column(Date, nullable=False)
    # region_id = Column(Integer, ForeignKey("region.id"), nullable=True)
    # created_at = Column(
    #     DateTime,
    #     server_default=text("CURRENT_TIMESTAMP"),
    #     nullable=False,
    # )
    # updated_at = Column(
    #     DateTime,
    #     server_default=text("CURRENT_TIMESTAMP"),
    #     onupdate=func.current_timestamp(),
    #     nullable=False,
    # )
    # is_active = Column(Boolean, server_default=text("TRUE"), nullable=False)
    # view_count = Column(Integer, server_default=text("0"), nullable=False)

    # # 관계 설정
    # region = relationship("Region")
    # timeline_items = relationship(
    #     "Timeline",
    #     back_populates="event",
    #     cascade="all, delete-orphan",
    # )
