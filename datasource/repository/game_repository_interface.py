from typing import Optional
from uuid import UUID
from domain.model.game import CurrentGame


class IGameRepository:
    def save_game(self, game: CurrentGame) -> None:
        raise NotImplementedError

    def get_game(self, game_id: UUID) -> Optional[CurrentGame]:
        raise NotImplementedError
