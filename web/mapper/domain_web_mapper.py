from domain.model.board import Board
from domain.model.game import CurrentGame
from web.model.game_dto import BoardDTO, GameDTO
from domain.model.game_state import GameState

class DomainWebMapper:
    @staticmethod
    def to_dto(domain_game: CurrentGame, winner: str = None) -> GameDTO:
        return GameDTO(
            id=domain_game.id,
            board=BoardDTO(matrix=[row[:] for row in domain_game.board.matrix]),
            winner=winner
        )

    @staticmethod
    def to_domain(dto: GameDTO) -> CurrentGame:
        return CurrentGame(
            id=dto.id,
            board=Board(matrix=[row[:] for row in dto.board.matrix]),
            state=GameState.PLAYER_TURN
        )
