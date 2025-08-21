"""
Greedy Solver for ColorTile Game
"""

from typing import List

from src.base.answer import Answer, Move

from .base_solver import BaseSolver


class GreedySolver(BaseSolver):
    """ColorTile game solver using greedy algorithm"""

    def solve(self, max_moves: int = 1000) -> Answer:
        """Solve using greedy algorithm and return Answer object"""
        moves_made = 0
        moves: List[Move] = []

        while moves_made < max_moves:
            valid_moves = self._find_all_valid_moves()
            if not valid_moves:
                break

            # Select the upper-rightmost move
            valid_moves.sort()
            row, col, expected_points = valid_moves[0]
            actual_points = self.click_with_cache_update(row, col)

            assert actual_points == expected_points
            assert actual_points > 0

            move = Move(row=row, col=col, points=actual_points)
            moves.append(move)
            moves_made += 1

        self.current_answer = Answer(moves)
        return self.current_answer
