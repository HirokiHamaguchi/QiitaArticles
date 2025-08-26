from typing import List, Optional, Tuple

from .base_solver import BaseSolver


class BidirectionalSolver(BaseSolver):
    def __init__(self, game, avoid_triple: bool = False):
        super().__init__(game)
        self.avoid_triple = avoid_triple
        self.sort_type = 0

    def select_func(
        self, valid_moves: List[Tuple[int, int, int]]
    ) -> Optional[Tuple[int, int, int]]:
        if not valid_moves:
            return None

        if self.moves_made <= int(1 / 3 * (self.game.board.TOTAL_TILES / 2)):
            self.sort_type = 0
        elif self.moves_made <= int(2 / 3 * (self.game.board.TOTAL_TILES / 2)):
            self.sort_type = 1
        else:
            self.sort_type ^= 1

        if self.sort_type == 0:
            sorted_moves = sorted(valid_moves, key=lambda x: +x[0] - x[1])
        else:
            sorted_moves = sorted(valid_moves, key=lambda x: -x[0] + x[1])

        return sorted_moves[0]
