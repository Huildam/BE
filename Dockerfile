# 베이스 이미지
FROM python:3.13.5-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성만 먼저 복사 → 캐시 활용
COPY app/requirements.txt .

# pip 업데이트 및 의존성 설치
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 전체 복사
COPY app/ .

# 로그가 버퍼링되지 않도록 설정
ENV PYTHONUNBUFFERED=1

# uvicorn --reload 옵션으로 코드 변경 시 자동 재시작
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
