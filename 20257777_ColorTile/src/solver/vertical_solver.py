"""
Vertical Solver for ColorTile Game
"""

from typing import List

from src.base.answer import Answer, Move
from src.base.tile import TileColor

from .base_solver import BaseSolver


class VerticalSolver(BaseSolver):
    """ColorTile game solver using vertical strategy (topmost → rightmost)"""

    def __init__(self, game, avoid_triple: bool = False):
        super().__init__(game)
        self.avoid_triple = avoid_triple

    def _check_would_cause_triple(self, row: int, col: int) -> bool:
        """Check if clicking at (row, col) would cause a 3-tile removal"""
        if not self.avoid_triple:
            return False

        removable_positions = self.game.board.find_removable_tiles(row, col)

        # Count tiles by color that would be removed
        color_counts: dict[TileColor, int] = {}
        for tile_row, tile_col in removable_positions:
            tile = self.game.board.get_tile(tile_row, tile_col)
            if tile is not None:
                color_counts[tile.color] = color_counts.get(tile.color, 0) + 1

        # Check if any color has 3 or more tiles that would be removed
        return any(count >= 3 for count in color_counts.values())

    def solve(self, max_moves: int = 1000) -> Answer:
        """Solve using vertical strategy (topmost → rightmost) and return Answer object"""
        moves_made = 0
        moves: List[Move] = []

        while moves_made < max_moves:
            valid_moves = self._find_all_valid_moves()
            if not valid_moves:
                break

            # Sort by row (ascending), then by column (descending) for topmost → rightmost
            valid_moves.sort(key=lambda x: (x[0], -x[1]))

            selected_move = None

            if self.avoid_triple:
                # Try to find a move that doesn't cause triple removal
                for row, col, expected_points in valid_moves:
                    if not self._check_would_cause_triple(row, col):
                        selected_move = (row, col, expected_points)
                        break

                # If all moves cause triple removal, select the best one anyway
                if selected_move is None:
                    selected_move = valid_moves[0]
            else:
                selected_move = valid_moves[0]

            row, col, expected_points = selected_move
            actual_points = self.click_with_cache_update(row, col)

            assert actual_points == expected_points
            assert actual_points > 0

            move = Move(row=row, col=col, points=actual_points)
            moves.append(move)
            moves_made += 1

        self.current_answer = Answer(moves)
        return self.current_answer
