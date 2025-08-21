"""
Board class for ColorTile game
"""

import copy
import random
from collections import defaultdict
from enum import Enum
from typing import DefaultDict, List, Optional, Tuple

from src.base.tile import Tile, TileColor


class BoardType(Enum):
    """Board configuration types"""

    PC = "pc"
    APP = "app"
    EXPERIMENT = "experiment"


class Board:
    """Represents the game board with configurable dimensions"""

    # Board configurations
    CONFIGS = {
        BoardType.PC: {
            "width": 23,
            "height": 15,
            "tiles_per_color": 20,
            "tiles_kind": 10,
        },
        BoardType.APP: {
            "width": 10,
            "height": 13,
            "tiles_per_color": 20,
            "tiles_kind": 5,
        },
        BoardType.EXPERIMENT: {
            "width": 6,
            "height": 5,
            "tiles_per_color": 10,
            "tiles_kind": 1,
        },
    }

    def __init__(self, seed: int, board_type: BoardType = BoardType.APP) -> None:
        """Initialize the board with specified configuration"""
        config = self.CONFIGS[board_type]
        self.WIDTH = config["width"]
        self.HEIGHT = config["height"]
        self.TOTAL_CELLS = self.WIDTH * self.HEIGHT
        self.TILES_PER_COLOR = config["tiles_per_color"]
        self.TILES_KIND = config["tiles_kind"]
        self.TOTAL_TILES = self.TILES_KIND * self.TILES_PER_COLOR

        self.grid: List[List[Optional[Tile]]] = [
            [None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)
        ]
        self.score = 0
        self.rng = random.Random(seed)  # Initialize with default seed
        self._place_tiles_randomly()

    def _place_tiles_randomly(self):
        """Randomly place 200 tiles (20 of each color) on the board"""
        tiles = []
        for color in list(TileColor)[: self.TILES_KIND]:
            for _ in range(self.TILES_PER_COLOR):
                tiles.append(Tile(color))
        self.rng.shuffle(tiles)

        positions = [
            (row, col) for row in range(self.HEIGHT) for col in range(self.WIDTH)
        ]
        self.rng.shuffle(positions)

        assert len(tiles) <= len(positions)
        for i, tile in enumerate(tiles):
            row, col = positions[i]
            self.grid[row][col] = tile

    def set_seed(self, seed: int) -> None:
        """Set the random seed for tile placement"""
        self.rng = random.Random(seed)

    def is_inside(self, row: int, col: int) -> bool:
        """Check if the position is within the board boundaries"""
        return 0 <= row < self.HEIGHT and 0 <= col < self.WIDTH

    def get_tile(self, row: int, col: int) -> Optional[Tile]:
        """Get the tile at the specified position"""
        return self.grid[row][col] if self.is_inside(row, col) else None

    def is_empty(self, row: int, col: int) -> bool:
        """Check if the cell at the specified position is empty"""
        return self.get_tile(row, col) is None

    def find_tiles_in_directions(
        self, row: int, col: int
    ) -> List[Tuple[int, int, Tile]]:
        """Find the nearest tiles in all 4 directions from the given position"""
        nearest_tiles = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            current_row, current_col = row + dr, col + dc
            while self.is_inside(current_row, current_col):
                tile = self.get_tile(current_row, current_col)
                if tile is not None:
                    nearest_tiles.append((current_row, current_col, tile))
                    break
                current_row += dr
                current_col += dc
        return nearest_tiles

    def _get_removable_positions_from_tiles(
        self, tiles: List[Tuple[int, int, Tile]]
    ) -> List[Tuple[int, int]]:
        """Get removable positions from a list of tiles by grouping by color"""
        counts: DefaultDict[TileColor, int] = defaultdict(int)
        for _row, _col, tile in tiles:
            counts[tile.color] += 1

        ret = []
        for tile_row, tile_col, tile in tiles:
            if counts[tile.color] >= 2:
                ret.append((tile_row, tile_col))
        return ret

    def find_removable_tiles(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Find tiles that can be removed when clicking at the given position"""
        if not self.is_empty(row, col):
            return []

        tiles = self.find_tiles_in_directions(row, col)
        return self._get_removable_positions_from_tiles(tiles)

    def click(self, row: int, col: int) -> int:
        """Click on the specified position and remove tiles if possible"""
        removable_positions = self.find_removable_tiles(row, col)

        if not removable_positions:
            return 0

        for tile_row, tile_col in removable_positions:
            self.grid[tile_row][tile_col] = None
        points = len(removable_positions)
        self.score += points

        return points

    def get_remaining_tiles(self) -> int:
        """Count the number of tiles remaining on the board"""
        return sum(
            1
            for row in range(self.HEIGHT)
            for col in range(self.WIDTH)
            if self.get_tile(row, col) is not None
        )

    def copy(self) -> "Board":
        """Create a deep copy of the board"""
        new_board = Board.__new__(Board)
        new_board.WIDTH = self.WIDTH
        new_board.HEIGHT = self.HEIGHT
        new_board.TOTAL_CELLS = self.TOTAL_CELLS
        new_board.TILES_PER_COLOR = self.TILES_PER_COLOR
        new_board.TILES_KIND = self.TILES_KIND
        new_board.TOTAL_TILES = self.TOTAL_TILES
        new_board.grid = copy.deepcopy(self.grid)
        new_board.score = self.score
        new_board.rng = random.Random()
        new_board.rng.setstate(self.rng.getstate())  # Copy RNG state
        return new_board
