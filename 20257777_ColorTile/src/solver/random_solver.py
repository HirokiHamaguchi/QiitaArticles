"""
Random Solver for ColorTile Game
"""

import random
from typing import List, Optional

from src.base.answer import Answer, Move

from .base_solver import BaseSolver


class RandomSolver(BaseSolver):
    """ColorTile game solver using random selection"""

    def __init__(self, game, seed: Optional[int] = None):
        super().__init__(game)
        self.rng = random.Random(seed)

    def solve(self, max_moves: int = 1000) -> Answer:
        """Solve using random move selection and return Answer object"""
        moves_made = 0
        moves: List[Move] = []

        while moves_made < max_moves:
            valid_moves = self._find_all_valid_moves()
            if not valid_moves:
                break

            # Randomly select a move from valid moves
            row, col, expected_points = self.rng.choice(valid_moves)
            actual_points = self.click_with_cache_update(row, col)

            assert actual_points == expected_points
            assert actual_points > 0

            move = Move(row=row, col=col, points=actual_points)
            moves.append(move)
            moves_made += 1

        self.current_answer = Answer(moves)
        return self.current_answer
