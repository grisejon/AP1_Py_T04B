from typing import Optional
from uuid import UUID
from domain.model.user import User

class IUserService:
    def create_user(self, login: str, password: str) -> User:
        raise NotImplementedError

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        raise NotImplementedError

    def get_user_by_login(self, login: str) -> Optional[User]:
        raise NotImplementedError
