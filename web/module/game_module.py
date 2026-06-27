from domain.service.game_service_interface import GameServiceInterface
from datasource.repository.game_repository import GameRepository
from domain.model.game import CurrentGame
from web.model.game_dto import GameDTO
from web.mapper.domain_web_mapper import DomainWebMapper
from domain.model.game_state import GameState

class GameModule:
    def __init__(self, service: GameServiceInterface, repository: GameRepository):
        self.service = service
        self.repository = repository

    def play_move(self, game_dto: GameDTO, user_id: None = None) -> GameDTO:
        previous_game = self.repository.get_game(game_dto.id)
        
        if previous_game is None:
            raise ValueError("Game not found")

        if previous_game.state in [GameState.DRAW, GameState.VICTORY]:
            winner = self.service.get_winner(previous_game)
            return DomainWebMapper.to_dto(previous_game, winner=winner)

        if previous_game.state == GameState.WAITING:
            raise ValueError("Game is waiting for another player to join")

        current_game = DomainWebMapper.to_domain(game_dto)
        current_game.state = previous_game.state
        current_game.player_one_id = previous_game.player_one_id
        current_game.player_two_id = previous_game.player_two_id
        current_game.player_one_symbol = previous_game.player_one_symbol
        current_game.player_two_symbol = previous_game.player_two_symbol
        current_game.current_turn_user_id = previous_game.current_turn_user_id
        current_game.against_computer = previous_game.against_computer

        if not self.service.validate_game(current_game, previous_game):
            raise ValueError("Invalid move: previous moves altered or incorrect move")
        
        if current_game.current_turn_user_id == current_game.player_one_id:
            current_game.current_turn_user_id = current_game.player_two_id
        else:
            current_game.current_turn_user_id = current_game.player_one_id

        self.repository.save_game(current_game)
        
        if not self.service.is_game_over(current_game):
            if current_game.against_computer:
                updated_game = self.service.get_next_move(current_game)
                self.repository.save_game(updated_game)
                current_game = updated_game
        
        if self.service.is_game_over(current_game):

            winner = self.service.get_winner(current_game)
            current_game.state = GameState.VICTORY if winner != "Draw" else GameState.DRAW
            self.repository.save_game(current_game)
            return DomainWebMapper.to_dto(current_game, winner=winner)
        
        return DomainWebMapper.to_dto(current_game)


