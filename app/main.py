from fastapi import FastAPI
from api import health

app = FastAPI()

# 테스트용 api 추가
app.include_router(health.router, prefix="/api")
