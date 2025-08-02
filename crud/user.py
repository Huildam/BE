from sqlalchemy.orm import Session
from models.user import User
from typing import List, Optional
from passlib.context import CryptContext

# 비밀번호 해싱을 위한 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_list(db: Session) -> List[User]:
    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, password: str, role: str = "user", region_id: Optional[int] = None) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        email=email,
        password_hash=hashed_password,
        role=role,
        region_id=region_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user 