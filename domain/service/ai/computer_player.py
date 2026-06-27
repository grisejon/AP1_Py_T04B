from typing import Tuple, List
from domain.model.game import CurrentGame
from domain.model.player_symbol import PlayerSymbol

class ComputerPlayer:
    PLAYER_SYMBOL = 1
    COMPUTER_SYMBOL = -1

    def get_best_move(self, game: CurrentGame) -> Tuple[int, int]:
        matrix = [row[:] for row in game.board.matrix]
        
        best_val = -float('inf')
        best_move = None
        
        for r in range(3):
            for c in range(3):
                if matrix[r][c] == 0:
                    matrix[r][c] = self.COMPUTER_SYMBOL
                    val = self._minimax(matrix, 0, False)
                    matrix[r][c] = 0
                    if val > best_val:
                        best_val = val
                        best_move = (r, c)
        
        if best_move is None:
            for r in range(3):
                for c in range(3):
                    if matrix[r][c] == 0:
                        return (r, c)
            
        return best_move

    def _evaluate(self, m: List[List[int]]) -> int:
        for i in range(3):
            s_row = sum(m[i])
            if abs(s_row) == 3:
                return 1 if s_row == self.COMPUTER_SYMBOL * 3 else -1
            s_col = sum(m[row][i] for row in range(3))
            if abs(s_col) == 3:
                return 1 if s_col == self.COMPUTER_SYMBOL * 3 else -1
        
        d1 = m[0][0] + m[1][1] + m[2][2]
        if abs(d1) == 3:
            return 1 if d1 == self.COMPUTER_SYMBOL * 3 else -1
        
        d2 = m[0][2] + m[1][1] + m[2][0]
        if abs(d2) == 3:
            return 1 if d2 == self.COMPUTER_SYMBOL * 3 else -1
            
        return 0

    def _minimax(self, m: List[List[int]], depth: int, is_max: bool) -> float:
        score = self._evaluate(m)
        if score != 0:
            return score
        if all(all(cell != 0 for cell in row) for row in m):
            return 0

        if is_max:
            best = -float('inf')
            for r in range(3):
                for c in range(3):
                    if m[r][c] == 0:
                        m[r][c] = self.COMPUTER_SYMBOL
                        best = max(best, self._minimax(m, depth + 1, False))
                        m[r][c] = 0
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if m[r][c] == 0:
                        m[r][c] = self.PLAYER_SYMBOL
                        best = min(best, self._minimax(m, depth + 1, True))
                        m[r][c] = 0
            return best
