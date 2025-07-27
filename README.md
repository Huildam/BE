# FastAPI Docker 프로젝트

FastAPI와 Docker를 사용한 백엔드 개발 환경입니다.

## 기능

- FastAPI 웹 프레임워크
- PostgreSQL 데이터베이스
- pgAdmin 데이터베이스 관리 도구
- Docker 컨테이너화
- 자동 리로드 개발 환경

## 요구사항

- Docker
- Docker Compose

## 🛠️ 설치 및 실행

### 1. Docker 컨테이너 실행
```bash
# 모든 서비스 시작
docker-compose up -d

```

### 2. 애플리케이션 접속

- **FastAPI 애플리케이션**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050
  - 이메일: Huildam@admin.com
  - 비밀번호: qwer123!

## pgAdmin 사용법

pgAdmin은 웹 기반의 PostgreSQL 관리 도구입니다. 아래와 같이 접속 및 데이터베이스 서버를 등록할 수 있습니다.

1. 브라우저에서 [http://localhost:5050](http://localhost:5050) 접속
2. 로그인 정보 입력
   - 이메일: **Huildam@admin.com**
   - 비밀번호: **qwer123!**
3. 좌측 상단 "Add New Server" 클릭
4. General 탭에서 이름 입력 
5. Connection 탭에서 아래 정보 입력
   - Host name/address: **postgres**
   - Port: **5432**
   - Username: **Huildam**
   - Password: **qwer123!**
6. 저장 후 접속하면 DB를 관리할 수 있습니다.

## 프로젝트 구조

```
.
├── api/
│   └── v1/
│       ├── health.py
│       └── __init__.py
├── core/
│   ├── config.py
│   └── __init__.py
├── models/ 
│   ├── user.py
│   └── __init__.py
├── crud/
│   ├── user.py
│   └── __init__.py
├── db/
│   ├── session.py
│   └── __init__.py
├── schemas/
│   ├── user.py
│   └── __init__.py
├── services/
│   └── (서비스별 파일)
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```
## 주요 폴더별 역할

| 폴더         | 핵심 역할                                      |
| ------------ | ---------------------------------------------- |
| `core/`      | 환경설정 및 로깅                                |
| `models/`    | DB 테이블 구조 정의                             |
| `schemas/`   | API 요청/응답 구조 정의 (Pydantic)              |
| `crud/`      | DB와 직접 상호작용하는 함수들                   |
| `db/`        | DB 세션 및 메타 설정 (연결, 초기화 등)           |

### 개발 명령어

```bash
# 컨테이너 빌드 및 시작
docker-compose up --build

# 백그라운드에서 실행
docker-compose up -d

# 특정 서비스만 재시작
docker-compose restart app

# 컨테이너 중지
docker-compose down

# 컨테이너 및 볼륨 삭제
docker-compose down -v

# 로그 확인
docker-compose logs app
docker-compose logs db
```

## 데이터베이스 설정

### PostgreSQL 연결 정보
- **호스트**: localhost (또는 db)
- **포트**: 5432
- **데이터베이스**: Huildam
- **사용자**: Huildam
- **비밀번호**: qwer123!

## 테스트

```bash
# 컨테이너 내에서 테스트 실행
docker-compose exec app pytest

# 특정 테스트 파일 실행
docker-compose exec app pytest test_main.py
```

## API 엔드포인트

- `GET /`: 루트 엔드포인트
- `GET /check-postgres`: 디비 연결 확인
- `GET /docs`: API 문서 (Swagger UI)

## 환경 변수

주요 환경 변수들은 `docker-compose.yml`에서 설정되어 있습니다:

- `DATABASE_URL`: PostgreSQL 연결 문자열

## 문제 해결

### 포트 충돌
포트가 이미 사용 중인 경우 `docker-compose.yml`에서 포트를 변경하세요.

### 컨테이너 재빌드
```bash
# 이미지 재빌드
docker-compose build --no-cache

# 컨테이너 재시작
docker-compose up -d
```

## 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Docker 공식 문서](https://docs.docker.com/)
- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)

