from typing import Optional
from uuid import UUID
from datasource.model.game_data import GameData
from datasource.db import db
from datasource.mapper.domain_data_mapper import DomainDataMapper
from domain.model.game import CurrentGame
from datasource.repository.game_repository_interface import IGameRepository


class GameRepository(IGameRepository):
    def __init__(self):
        pass

    def save_game(self, game: CurrentGame):
        data = DomainDataMapper.to_data(game)
        existing = db.session.get(GameData, data.id)
        if existing:
            existing.board_matrix = data.board_matrix
            existing.state = data.state
            existing.player_one_id = data.player_one_id
            existing.player_two_id = data.player_two_id
            existing.player_one_symbol = data.player_one_symbol
            existing.player_two_symbol = data.player_two_symbol
            existing.current_turn_user_id = data.current_turn_user_id
        else:
            db.session.add(data)
        db.session.commit()

    def get_game(self, game_id: UUID) -> Optional[CurrentGame]:
        data = db.session.get(GameData, game_id)
        return DomainDataMapper.to_domain(data) if data else None
