from dataclasses import dataclass
from typing import List
from uuid import UUID

@dataclass
class BoardDTO:
    matrix: List[List[int]]

@dataclass
class GameDTO:
    id: UUID
    board: BoardDTO
    winner: str = None

