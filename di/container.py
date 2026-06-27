from datasource.repository.game_repository import GameRepository
from domain.service.game_service_impl import GameServiceImpl
from domain.service.user_service_impl import UserServiceImpl
from domain.service.authorization_service import AuthorizationService


class Container:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
            cls._instance.repository = GameRepository()
            cls._instance.service = GameServiceImpl(cls._instance.repository)
            cls._instance.user_service = UserServiceImpl()
            cls._instance.auth_service = AuthorizationService(cls._instance.user_service)
        return cls._instance


container = Container()
