from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def check_health():
    """
    서비스 정상 동작 여부를 확인합니다.
    """
    return "OK~"
