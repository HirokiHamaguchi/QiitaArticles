"""
Base Solver for ColorTile Game
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from src.base.answer import Answer, Move
from src.base.game import Game
from src.base.tile import Tile, TileColor


class BaseSolver(ABC):
    def __init__(self, game: Game):
        self.game = game
        self.current_answer: Optional[Answer] = None
        self._direction_tiles_cache: Optional[
            List[List[List[Optional[Tuple[int, int, Tile]]]]]
        ] = None

    @abstractmethod
    def select_func(
        self, valid_moves: List[Tuple[int, int, int]]
    ) -> Optional[Tuple[int, int, int]]:
        if not valid_moves:
            return None
        return valid_moves[0]

    def solve(self, max_moves: int) -> Answer:
        """Generic solve method for strategy-based solvers"""

        self.moves_made = 0
        moves = []
        while self.moves_made < max_moves:
            valid_moves = self._find_all_valid_moves()
            if not valid_moves:
                break

            if getattr(self, "avoid_triple", False):
                new_valid_moves: List[Tuple[int, int, int]] = []
                for row, col, expected_points in valid_moves:
                    if not self._check_would_cause_triple(row, col):
                        new_valid_moves.append((row, col, expected_points))
                if new_valid_moves:
                    valid_moves = new_valid_moves

            selected_move = self.select_func(valid_moves)
            if selected_move is None:
                break

            row, col, expected_points = selected_move
            actual_points = self._click_with_cache_update(row, col)
            assert actual_points == expected_points
            assert actual_points > 0
            move = Move(row=row, col=col, points=actual_points)
            moves.append(move)
            self.moves_made += 1

        self.current_answer = Answer(moves)
        return self.current_answer

    def reset(self):
        """Reset the solver and game"""
        self.game.reset()
        self.current_answer = None
        self._direction_tiles_cache = None

    def _click_with_cache_update(self, row: int, col: int) -> int:
        """Click and update the direction tiles cache efficiently"""
        removable_positions = self.game.board.find_removable_tiles(row, col)
        points = self.game.click(row, col)
        if self._direction_tiles_cache is not None and removable_positions:
            self._update_direction_tiles_for_removed_positions(removable_positions)
        return points

    def _scan_direction(
        self,
        direction_tiles: List[List[Optional[Tuple[int, int, Tile]]]],
        dr: int,
        dc: int,
        row_range: range,
        col_range: range,
    ):
        """Scan a direction and populate direction_tiles array"""
        if dr != 0:  # 縦方向（上下）
            for col in col_range:
                nearest = None
                for row in row_range:
                    tile = self.game.board.get_tile(row, col)
                    if tile is not None:
                        nearest = (row, col, tile)
                        direction_tiles[row][col] = None
                    else:
                        direction_tiles[row][col] = nearest
        else:  # 横方向（左右）
            for row in row_range:
                nearest = None
                for col in col_range:
                    tile = self.game.board.get_tile(row, col)
                    if tile is not None:
                        nearest = (row, col, tile)
                        direction_tiles[row][col] = None
                    else:
                        direction_tiles[row][col] = nearest

    def _preprocess_next_tiles(
        self,
    ) -> List[List[List[Optional[Tuple[int, int, Tile]]]]]:
        """Preprocess to find nearest tiles in all directions for each position"""
        H, W = self.game.board.HEIGHT, self.game.board.WIDTH
        direction_configs = self._get_direction_configs()
        next_tiles = []

        for dr, dc, row_range, col_range in direction_configs:
            direction_tiles: List[List[Optional[Tuple[int, int, Tile]]]] = [
                [None] * W for _ in range(H)
            ]
            self._scan_direction(direction_tiles, dr, dc, row_range, col_range)
            next_tiles.append(direction_tiles)

        return next_tiles

    def _get_direction_configs(self):
        """Get the common direction configurations"""
        H, W = self.game.board.HEIGHT, self.game.board.WIDTH
        return [
            (-1, 0, range(H), range(W)),  # 上方向
            (1, 0, range(H - 1, -1, -1), range(W)),  # 下方向
            (0, -1, range(H), range(W)),  # 左方向
            (0, 1, range(H), range(W - 1, -1, -1)),  # 右方向
        ]

    def _update_direction_tiles_for_removed_positions(
        self, removed_positions: List[Tuple[int, int]]
    ):
        """Update direction tiles cache for removed tile positions"""
        if self._direction_tiles_cache is None:
            return

        direction_configs = self._get_direction_configs()

        for removed_row, removed_col in removed_positions:
            for dir_idx, (dr, dc, row_range, col_range) in enumerate(direction_configs):
                cache = self._direction_tiles_cache[dir_idx]

                if dr != 0:
                    col = removed_col
                    self._scan_direction(cache, dr, dc, row_range, range(col, col + 1))
                else:
                    row = removed_row
                    self._scan_direction(cache, dr, dc, range(row, row + 1), col_range)

    def _get_or_create_direction_tiles(
        self,
    ) -> List[List[List[Optional[Tuple[int, int, Tile]]]]]:
        """Get cached direction tiles or create if not exists"""
        if self._direction_tiles_cache is None:
            self._direction_tiles_cache = self._preprocess_next_tiles()
        return self._direction_tiles_cache

    def _find_all_valid_moves(self) -> List[Tuple[int, int, int]]:
        """Find all valid moves and their potential points (optimized version)"""
        # キャッシュされた方向タイルを取得
        direction_tiles_list = self._get_or_create_direction_tiles()

        valid_moves = []
        for row in range(self.game.board.HEIGHT):
            for col in range(self.game.board.WIDTH):
                if self.game.board.is_empty(row, col):
                    tiles = []
                    for direction_tiles in direction_tiles_list:
                        nearest = direction_tiles[row][col]
                        if nearest is not None:
                            tiles.append(nearest)

                    removable_positions = (
                        self.game.board._get_removable_positions_from_tiles(tiles)
                    )

                    if removable_positions:
                        points = len(removable_positions)
                        valid_moves.append((row, col, points))

        return valid_moves

    def _check_would_cause_triple(self, row: int, col: int) -> bool:
        """Check if clicking at (row, col) would cause a 3-tile removal"""
        if not getattr(self, "avoid_triple", False):
            return False

        color_counts: dict[TileColor, int] = {}
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            tile = self.game.board.get_tile(new_row, new_col)
            if tile is not None:
                color_counts[tile.color] = color_counts.get(tile.color, 0) + 1
        return any(count >= 3 for count in color_counts.values())
