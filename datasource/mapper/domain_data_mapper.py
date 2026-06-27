from domain.model.board import Board
from domain.model.game import CurrentGame
from datasource.model.game_data import GameData
from domain.model.game_state import GameState
from domain.model.player_symbol import PlayerSymbol

class DomainDataMapper:
    @staticmethod
    def to_data(domain_game: CurrentGame) -> GameData:
        return GameData(
            id=domain_game.id,
            board_matrix=[row[:] for row in domain_game.board.matrix],
            state=domain_game.state.value,
            player_one_id=domain_game.player_one_id,
            player_two_id=domain_game.player_two_id,
            player_one_symbol=domain_game.player_one_symbol.value if domain_game.player_one_symbol else None,
            player_two_symbol=domain_game.player_two_symbol.value if domain_game.player_two_symbol else None,
            current_turn_user_id=domain_game.current_turn_user_id
        )

    @staticmethod
    def to_domain(data_game: GameData) -> CurrentGame:
        return CurrentGame(
            id=data_game.id,
            board=Board(matrix=[row[:] for row in data_game.board_matrix]),
            state=GameState(data_game.state),
            player_one_id=data_game.player_one_id,
            player_two_id=data_game.player_two_id,
            player_one_symbol=PlayerSymbol(data_game.player_one_symbol) if data_game.player_one_symbol else None,
            player_two_symbol=PlayerSymbol(data_game.player_two_symbol) if data_game.player_two_symbol else None,
            current_turn_user_id=data_game.current_turn_user_id
        )
