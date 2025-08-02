
from typing import List
from sqlalchemy.orm import joinedload

from pytest import Session
from models.region import Region


def get_all_region_where_parent_id_is_not_null(db: Session) -> List[Region]:
    return db.query(Region) \
        .filter(Region.parent_id.isnot(None)) \
        .options(joinedload(Region.parent)) \
        .all()