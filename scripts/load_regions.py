from db.session import SessionLocal
from utils.region_loader import load_regions_from_file
from pathlib import Path

def main():
    db = SessionLocal()
    try:
        filepath = Path(__file__).parent.parent / "data" / "korea_regions.txt"
        load_regions_from_file(str(filepath), db)
        print("✅ 지역 데이터 로딩 완료.")
    except Exception as e:
        print("❌ 에러 발생:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
