"""
Game Analysis Utilities for ColorTile Game
"""

from collections import defaultdict
from typing import Any, Dict

from src.base.game import Game
from src.base.tile import TileColor


class GameAnalyzer:
    """Utility class for analyzing game states and failure conditions"""

    def __init__(self, game: Game):
        self.game = game

    def count_remaining_tiles_by_color(self) -> Dict[TileColor, int]:
        """Count remaining tiles for each color"""
        color_counts: Dict[TileColor, int] = defaultdict(int)

        for row in range(self.game.board.HEIGHT):
            for col in range(self.game.board.WIDTH):
                tile = self.game.board.get_tile(row, col)
                if tile is not None:
                    color_counts[tile.color] += 1

        return dict(color_counts)

    def has_odd_parity_failure(self) -> bool:
        """Check if game has failed due to odd parity (odd number of tiles for any color)"""
        color_counts = self.count_remaining_tiles_by_color()

        # Check if any color has an odd number of remaining tiles
        return any(count % 2 == 1 for count in color_counts.values())

    def has_placement_failure(self) -> bool:
        """Check if game has failed due to placement (no valid moves possible)"""
        # Check if there are any valid moves
        for row in range(self.game.board.HEIGHT):
            for col in range(self.game.board.WIDTH):
                if self.game.board.is_empty(row, col):
                    removable_tiles = self.game.board.find_removable_tiles(row, col)
                    if removable_tiles:
                        return False

        return True

    def has_adjacent_pairs(self) -> bool:
        """Check if there are adjacent tiles of the same color remaining"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for row in range(self.game.board.HEIGHT):
            for col in range(self.game.board.WIDTH):
                tile = self.game.board.get_tile(row, col)
                if tile is not None:
                    # Check all 4 directions for adjacent tiles of same color
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if self.game.board.is_inside(new_row, new_col):
                            adjacent_tile = self.game.board.get_tile(new_row, new_col)
                            if (
                                adjacent_tile is not None
                                and adjacent_tile.color == tile.color
                            ):
                                return True

        return False

    def analyze_game_result(self) -> Dict[str, Any]:
        """Comprehensive analysis of the game result"""
        remaining_tiles = self.game.get_remaining_tiles()
        score = self.game.get_score()

        analysis = {
            "total_remaining_tiles": remaining_tiles,
            "final_score": score,
            "is_complete_clear": remaining_tiles == 0,
            "has_odd_parity_failure": False,
            "has_placement_failure": False,
            "has_adjacent_pairs": False,
            "color_counts": {},
        }

        # Only analyze failure conditions if game is not completely cleared
        if remaining_tiles > 0:
            analysis.update(
                {
                    "has_odd_parity_failure": self.has_odd_parity_failure(),
                    "has_placement_failure": self.has_placement_failure(),
                    "has_adjacent_pairs": self.has_adjacent_pairs(),
                    "color_counts": self.count_remaining_tiles_by_color(),
                }
            )

        return analysis
