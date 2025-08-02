
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from crud.region import get_all_region_where_parent_id_is_not_null
from db.session import get_db
from schemas.region import RegionPairResponse


router = APIRouter()

@router.get("", response_model=List[RegionPairResponse], status_code=200)
def get_total_region_pair(db: Session = Depends(get_db)) -> List[RegionPairResponse]:
    # todo: parent_id가 null이 아닌 모든 레코드에 대해, 
    # 그 레코드의 id와 서울시 **구, 대전광역시 **구와 같이 name값을 만들어 반환하는 함수 작성
    regions = get_all_region_where_parent_id_is_not_null(db)

    pairs: List[RegionPairResponse] = []
    for region in regions:
        # "서울시 강남구", "대전광역시 중구" 등으로 부모-자식 구 이름 결합
        full_name = f"{region.parent.name} {region.name}"
        pairs.append(RegionPairResponse(id=region.id, name=full_name))

    return pairs