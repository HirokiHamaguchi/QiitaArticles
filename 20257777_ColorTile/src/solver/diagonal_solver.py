from typing import List, Optional, Tuple

from .base_solver import BaseSolver


class DiagonalSolver(BaseSolver):
    def __init__(self, game, avoid_triple: bool = False):
        super().__init__(game)
        self.avoid_triple = avoid_triple

    def select_func(
        self, valid_moves: List[Tuple[int, int, int]]
    ) -> Optional[Tuple[int, int, int]]:
        if not valid_moves:
            return None

        sorted_moves = sorted(valid_moves, key=lambda x: x[0] - x[1])
        return sorted_moves[0]
