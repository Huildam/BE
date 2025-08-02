import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal
from crud.user import create_user

def main():
    db = SessionLocal()
    try:
        print("📍 사용할 지역 ID: 244 (서귀포시)")
        
        # 서귀포시 사용자 생성
        test_user = create_user(
            db=db,
            email="user@example.com",
            password="user123",
            role="user",
            region_id=244
        )
        print(f"✅ 테스트 사용자 생성 완료: {test_user.email} (지역: 서귀포시)")
        
        # 서귀포시 기자 생성
        reporter_user = create_user(
            db=db,
            email="reporter@example.com",
            password="reporter123",
            role="reporter",
            region_id=244
        )
        print(f"✅ 기자 사용자 생성 완료: {reporter_user.email} (지역: 서귀포시)")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 