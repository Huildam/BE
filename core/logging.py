import logging

# uvicorn이 아닌 모듈 전반에 적용될 기본 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)  # 보통 'db.session' 이름으로 찍힙니다.
