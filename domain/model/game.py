from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from domain.model.board import Board
from domain.model.game_state import GameState
from domain.model.player_symbol import PlayerSymbol

@dataclass
class CurrentGame:
    id: UUID
    board: Board
    state: GameState
    player_one_id: Optional[UUID] = None
    player_two_id: Optional[UUID] = None
    player_one_symbol: Optional[PlayerSymbol] = None
    player_two_symbol: Optional[PlayerSymbol] = None
    current_turn_user_id: Optional[UUID] = None
    against_computer: bool = False
