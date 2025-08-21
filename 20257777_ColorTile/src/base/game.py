"""
ColorTile Game main class
"""

from typing import List, Tuple

from src.base.board import Board, BoardType


class Game:
    """Main game class for ColorTile"""

    def __init__(self, seed: int, board_type: BoardType = BoardType.APP) -> None:
        """Initialize a new game"""
        self.board = Board(seed, board_type)
        self.initial_board = self.board.copy()
        self.move_history: List[Tuple[int, int, int]] = []  # (row, col, points)

    def click(self, row: int, col: int) -> int:
        """Click on the specified position"""
        points = self.board.click(row, col)
        self.move_history.append((row, col, points))
        return points

    def simulate_moves(self, moves: List[Tuple[int, int]]) -> None:
        """Simulate a sequence of moves and return points earned for each move"""
        for row, col in moves:
            self.click(row, col)

    def get_score(self) -> int:
        """Get the current score"""
        return self.board.score

    def get_remaining_tiles(self) -> int:
        """Get the number of tiles remaining on the board"""
        return self.board.get_remaining_tiles()

    def get_move_history(self) -> List[Tuple[int, int, int]]:
        """Get the history of moves"""
        return self.move_history.copy()

    def get_initial_board(self) -> Board:
        """Get a copy of the initial board state"""
        return self.initial_board.copy()

    def reset(self):
        """Reset the game to initial state"""
        self.board = self.initial_board.copy()
        self.move_history = []

    def preview_click(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Preview which tiles would be removed if clicking at the given position"""
        return self.board.find_removable_tiles(row, col)
