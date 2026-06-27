from typing import Optional
from uuid import UUID, uuid4
from domain.model.user import User
from domain.service.user_service_interface import IUserService
from datasource.model.user_data import UserData
from datasource.db import db

class UserServiceImpl(IUserService):
    def create_user(self, login: str, password: str) -> User:
        user_id = uuid4()
        user_data = UserData(id=user_id, login=login, password=password)
        db.session.add(user_data)
        db.session.commit()
        return User(id=user_id, login=login, password=password)

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        data = db.session.get(UserData, user_id)
        return User(id=data.id, login=data.login, password=data.password) if data else None

    def get_user_by_login(self, login: str) -> Optional[User]:
        data = UserData.query.filter_by(login=login).first()
        return User(id=data.id, login=data.login, password=data.password) if data else None
