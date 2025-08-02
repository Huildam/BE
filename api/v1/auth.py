from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from db.session import get_db
from crud.user import authenticate_user, get_user_by_id
from schemas.auth import LoginRequest, LoginResponse, UserResponse
from models.user import User

router = APIRouter()

# 간단한 세션 저장소 (MVP용)
user_sessions = {}


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다"
        )
    
    # 세션 ID 생성 (간단한 방식)
    session_id = f"session_{user.id}_{request.client.host}"
    user_sessions[session_id] = user.id
    
    return LoginResponse(
        access_token=session_id,
        user_id=user.id,
        email=user.email,
        role=user.role,
        region_id=user.region_id
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Authorization 헤더에서 세션 ID 가져오기
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 정보가 없습니다"
        )
    
    session_id = auth_header.replace("Bearer ", "")
    user_id = user_sessions.get(session_id)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 세션입니다"
        )
    
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        region_id=user.region_id,
        created_at=user.created_at.isoformat()
    )


@router.post("/logout")
def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        session_id = auth_header.replace("Bearer ", "")
        if session_id in user_sessions:
            del user_sessions[session_id]
    
    return {"message": "로그아웃 완료"} 