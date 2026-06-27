import base64
from typing import Optional
from uuid import UUID
from domain.service.user_service_interface import IUserService
from web.model.sign_up_request import SignUpRequest

class AuthorizationService:
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def register(self, request: SignUpRequest) -> bool:
        try:
            if self.user_service.get_user_by_login(request.login):
                return False
            self.user_service.create_user(request.login, request.password)
            return True
        except Exception:
            return False

    def authorize(self, auth_header: str) -> Optional[UUID]:
        try:
            if not auth_header or not auth_header.startswith("Basic "):
                return None
            
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            login, password = decoded_credentials.split(":", 1)
            
            user = self.user_service.get_user_by_login(login)
            if user and user.password == password:
                return user.id
        except Exception:
            pass
        return None
