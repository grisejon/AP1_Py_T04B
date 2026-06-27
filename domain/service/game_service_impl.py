from typing import List, Optional
from uuid import UUID, uuid4
from domain.model.board import Board
from domain.model.game import CurrentGame
from domain.service.game_service_interface import GameServiceInterface
from datasource.repository.game_repository import GameRepository
from domain.model.game_state import GameState
from domain.model.player_symbol import PlayerSymbol
from datasource.model.game_data import GameData
from datasource.mapper.domain_data_mapper import DomainDataMapper
from domain.service.ai.computer_player import ComputerPlayer


class GameServiceImpl(GameServiceInterface):
    PLAYER = 1
    COMPUTER = -1

    def __init__(self, repository: GameRepository):
        self.repository = repository

    def create_game(self, user_id: UUID, against_computer: bool) -> CurrentGame:
        game_id = uuid4()
        board = Board([[0]*3 for _ in range(3)])

        if against_computer:
            state = GameState.PLAYER_TURN
            player_one_id = user_id
            player_one_symbol = PlayerSymbol.X
            current_turn_id = user_id
        else:
            state = GameState.WAITING
            player_one_id = user_id
            player_one_symbol = PlayerSymbol.X
            current_turn_id = None

        game = CurrentGame(
            id=game_id,
            board=board,
            state=state,
            player_one_id=player_one_id,
            player_one_symbol=player_one_symbol,
            current_turn_user_id=current_turn_id,
            against_computer=against_computer
        )
        self.repository.save_game(game)
        return game

    def get_game(self, game_id: UUID) -> Optional[CurrentGame]:
        return self.repository.get_game(game_id)

    def validate_game(self, current_game: CurrentGame, previous_game: CurrentGame) -> bool:
        curr_matrix = current_game.board.matrix
        prev_matrix = previous_game.board.matrix
        
        diffs = 0
        for r in range(3):
            for c in range(3):
                if prev_matrix[r][c] != 0 and prev_matrix[r][c] != curr_matrix[r][c]:
                    return False
                if prev_matrix[r][c] == 0 and curr_matrix[r][c] != 0:
                    current_symbol = 0
                    if current_game.current_turn_user_id == current_game.player_one_id:
                        current_symbol = 1 if current_game.player_one_symbol == PlayerSymbol.X else -1
                    elif current_game.current_turn_user_id == current_game.player_two_id:
                        current_symbol = 1 if current_game.player_two_symbol == PlayerSymbol.X else -1
                    
                    if curr_matrix[r][c] != current_symbol:
                        return False
                    diffs += 1
        
        return diffs == 1

    def is_game_over(self, game: CurrentGame) -> bool:
        matrix = game.board.matrix
        for i in range(3):
            if abs(sum(matrix[i])) == 3: return True
            if abs(sum(matrix[row][i] for row in range(3))) == 3: return True
        if abs(matrix[0][0] + matrix[1][1] + matrix[2][2]) == 3: return True
        if abs(matrix[0][2] + matrix[1][1] + matrix[2][0]) == 3: return True
        if all(all(cell != 0 for cell in row) for row in matrix): return True
        return False

    def get_winner(self, game: CurrentGame) -> Optional[str]:
        matrix = game.board.matrix
        winning_symbol = None
        
        for i in range(3):
            s_row = sum(matrix[i])
            if abs(s_row) == 3:
                winning_symbol = 1 if s_row == 3 else -1
                break
            s_col = sum(matrix[row][i] for row in range(3))
            if abs(s_col) == 3:
                winning_symbol = 1 if s_col == 3 else -1
                break
        
        if not winning_symbol:
            d1 = matrix[0][0] + matrix[1][1] + matrix[2][2]
            if abs(d1) == 3:
                winning_symbol = 1 if d1 == 3 else -1
            else:
                d2 = matrix[0][2] + matrix[1][1] + matrix[2][0]
                if abs(d2) == 3:
                    winning_symbol = 1 if d2 == 3 else -1
        
        if winning_symbol is not None:
            if game.against_computer:
                return "Player" if winning_symbol == 1 else "Computer"
            
            # For PvP, we identify who has the winning symbol
            # Player 1 always starts with X (1) according to create_game
            return "Player 1" if winning_symbol == 1 else "Player 2"
        
        return "Draw" if all(all(cell != 0 for cell in row) for row in matrix) else None

    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        ai = ComputerPlayer()
        best_move = ai.get_best_move(game)
        
        matrix = [row[:] for row in game.board.matrix]
        if best_move:
            matrix[best_move[0]][best_move[1]] = -1
            
        game.board.matrix = matrix
        return game

    def get_available_games(self) -> List[CurrentGame]:
        games_data = GameData.query.filter_by(state=GameState.WAITING.value).all()
        return [DomainDataMapper.to_domain(gd) for gd in games_data]

    def get_all_games(self) -> List[CurrentGame]:
        games_data = GameData.query.all()
        return [DomainDataMapper.to_domain(gd) for gd in games_data]

    def join_game(self, game_id: UUID, user_id: UUID) -> Optional[CurrentGame]:
        game = self.repository.get_game(game_id)
        if not game or game.state != GameState.WAITING or game.player_one_id == user_id:
            return None
        
        game.player_two_id = user_id
        game.player_two_symbol = PlayerSymbol.O
        game.state = GameState.PLAYER_TURN
        game.current_turn_user_id = game.player_one_id
        
        self.repository.save_game(game)
        return game
