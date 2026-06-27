from enum import Enum

class GameState(Enum):
    WAITING = "waiting"
    PLAYER_TURN = "player_turn"
    DRAW = "draw"
    VICTORY = "victory"
