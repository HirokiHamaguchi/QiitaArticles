from typing import List, Optional, Tuple

from .base_solver import BaseSolver


class CornerSolver(BaseSolver):
    def __init__(self, game, avoid_triple: int):
        super().__init__(game)
        self.avoid_triple = avoid_triple
        self.sort_type = 0

    def select_func(
        self, valid_moves: List[Tuple[int, int, int]]
    ) -> Optional[Tuple[int, int, int]]:
        if not valid_moves:
            return None

        if self.sort_type == 0:
            ret = min(valid_moves, key=lambda x: +x[0] - x[1])
        elif self.sort_type == 1:
            ret = min(valid_moves, key=lambda x: -x[0] - x[1])
        elif self.sort_type == 2:
            ret = min(valid_moves, key=lambda x: -x[0] + x[1])
        else:
            ret = min(valid_moves, key=lambda x: +x[0] + x[1])

        self.sort_type = (self.sort_type + 1) % 4
        return ret
