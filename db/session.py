import logging
import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.logging import logger
from db.base import Base

from models.user import User
from models.region import Region

DATABASE_URL = "postgresql+psycopg2://Huildam:qwer123!@postgres:5432/Huildam"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_table():
    logger.info("init_table() called.")
    logger.info("Checking and creating tables if not exist...")
    Base.metadata.create_all(bind=engine)  # ✅ 안전하게 테이블 생성
    logger.info("Tables checked/created successfully.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def connect_postgres():
    env = os.getenv("ENV", "local")
    host = "postgres" if env == "docker" else "localhost"
    try:
        conn = psycopg2.connect(
            host=host,
            database="Huildam",  # docker-compose.yml의 DB명과 맞춰주세요
            user="Huildam",  # docker-compose.yml의 사용자와 맞춰주세요
            password="qwer123!",  # docker-compose.yml의 비밀번호와 맞춰주세요
        )
        conn.close()
        return True, f"PostgreSQL 연결 성공: 환경={env}, host={host}"
    except Exception as e:
        return False, f"PostgreSQL 연결 실패: {e}"
