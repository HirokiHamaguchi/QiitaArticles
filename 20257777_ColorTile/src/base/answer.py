"""
ColorTile Game Answer - Solution representation
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Move:
    """Represents a single move in the game"""

    row: int
    col: int
    points: int

    def __str__(self) -> str:
        return f"({self.row}, {self.col})({self.points}pt)"


@dataclass
class Answer:
    """Represents a complete solution to the ColorTile game"""

    moves: List[Move]

    def is_valid(self) -> bool:
        """Check if all moves in the solution are valid (remove at least 1 tile)"""
        return all(move.points > 0 for move in self.moves)

    def __str__(self) -> str:
        assert self.is_valid()
        return " → ".join(str(move) for move in self.moves)
