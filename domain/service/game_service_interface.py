from abc import ABC, abstractmethod
from domain.model.game import CurrentGame
from typing import Optional, List
from uuid import UUID

class GameServiceInterface(ABC):
    @abstractmethod
    def create_game(self, user_id: UUID, against_computer: bool) -> CurrentGame:
        pass

    @abstractmethod
    def get_available_games(self) -> List[CurrentGame]:
        pass

    @abstractmethod
    def get_all_games(self) -> List[CurrentGame]:
        pass

    @abstractmethod
    def join_game(self, game_id: UUID, user_id: UUID) -> Optional[CurrentGame]:
        pass

    @abstractmethod
    def get_game(self, game_id: UUID) -> Optional[CurrentGame]:
        pass

    @abstractmethod
    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        pass

    @abstractmethod
    def validate_game(self, current_game: CurrentGame, previous_game: CurrentGame) -> bool:
        pass

    @abstractmethod
    def is_game_over(self, game: CurrentGame) -> bool:
        pass

    @abstractmethod
    def get_winner(self, game: CurrentGame) -> Optional[str]:
        pass
