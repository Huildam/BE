from models.user import User
from typing import List

def get_user_list() -> List[User]:
    # 예시 데이터
    return [
        User(id=1, username="testuser", email="test@example.com")
    ] 