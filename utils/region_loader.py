import csv
from models.region import Region
from sqlalchemy.orm import Session

def get_region_by_name_and_level(db, name, level, parent_id):
    return db.query(Region).filter_by(
        name=name,
        level=level,
        parent_id=parent_id
    ).first()


def load_regions_from_file(filepath: str, db: Session):
    region_id_map = {}

    with open(filepath, encoding='euc-kr') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # 헤더 건너뜀

        for row in reader:
            if len(row) < 3:
                continue

            _, full_name, status = row
            if status.strip() == '폐지':
                continue

            parts = full_name.strip().split()
            if not parts:
                continue

            sido = parts[0]
            sigungu = parts[1] if len(parts) > 1 else None

            # 시도 INSERT
            if sido and sido not in region_id_map:
                region = get_region_by_name_and_level(db, sido, 1, None)
                if not region:
                    region = Region(name=sido, level=1, parent_id=None)
                    db.add(region)
                    db.flush()
                region_id_map[sido] = region.id

            # 시군구 INSERT
            if sigungu:
                key = f"{sido}_{sigungu}"
                if key not in region_id_map:
                    parent_id = region_id_map[sido]
                    region = get_region_by_name_and_level(db, sigungu, 2, parent_id)
                    if not region:
                        region = Region(name=sigungu, level=2, parent_id=parent_id)
                        db.add(region)
                        db.flush()
                    region_id_map[key] = region.id

    db.commit()
