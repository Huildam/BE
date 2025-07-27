from fastapi import APIRouter
from db.session import connect_postgres

router = APIRouter()

@router.get("/")
def health():
    return {"status": "healthy", "message": "서버가 정상적으로 작동 중입니다"}

@router.get("/check-postgres")
def check_postgres():
    success, message = connect_postgres()
    return {"status": "success" if success else "fail", "message": message} 