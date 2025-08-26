import random
from typing import List, Optional, Tuple

from .base_solver import BaseSolver


class RandomSolver(BaseSolver):
    """ColorTile game solver using random selection"""

    def __init__(self, game, seed: Optional[int] = None, avoid_triple: bool = False):
        super().__init__(game)
        self.rng = random.Random(seed)
        self.avoid_triple = avoid_triple

    def select_func(
        self, valid_moves: List[Tuple[int, int, int]]
    ) -> Optional[Tuple[int, int, int]]:
        if not valid_moves:
            return None
        return self.rng.choice(valid_moves)
