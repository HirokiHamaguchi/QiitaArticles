"""
ANSI terminal-based visualizer for ColorTile game
"""

import time
from typing import Any

from src.base.answer import Answer
from src.vis.base import BaseVisualizer


class ANSIColors:
    """ANSI color codes for terminal display"""

    # Reset
    RESET = "\033[0m"

    # Text colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright text colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"

    # Cursor movement
    CLEAR_SCREEN = "\033[2J"
    CLEAR_LINE = "\033[K"
    HOME = "\033[H"
    SAVE_CURSOR = "\033[s"
    RESTORE_CURSOR = "\033[u"

    def __init__(self):
        """Initialize ANSIColors with a color map for tiles"""
        self.color_map = {
            "R": ANSIColors.BRIGHT_RED + "R" + ANSIColors.RESET,  # Red
            "B": ANSIColors.BRIGHT_BLUE + "B" + ANSIColors.RESET,  # Blue
            "G": ANSIColors.BRIGHT_GREEN + "G" + ANSIColors.RESET,  # Green
            "Y": ANSIColors.BRIGHT_YELLOW + "Y" + ANSIColors.RESET,  # Yellow
            "P": ANSIColors.BRIGHT_MAGENTA + "P" + ANSIColors.RESET,  # Purple
            "O": ANSIColors.YELLOW + "O" + ANSIColors.RESET,  # Orange
            "K": ANSIColors.MAGENTA + "K" + ANSIColors.RESET,  # Pink
            "C": ANSIColors.BRIGHT_CYAN + "C" + ANSIColors.RESET,  # Cyan
            "N": ANSIColors.BRIGHT_BLACK + "N" + ANSIColors.RESET,  # Brown
            "A": ANSIColors.WHITE + "A" + ANSIColors.RESET,  # Gray
            ".": ANSIColors.DIM + "." + ANSIColors.RESET,  # Empty
            "X": ANSIColors.BG_RED
            + " "
            + ANSIColors.RESET,  # Removed tile (red background)
        }

    def get_color(self, symbol: str) -> str:
        """Get the ANSI color code for a given tile symbol"""
        assert symbol in self.color_map, f"Symbol '{symbol}' not found in color map"
        return self.color_map.get(symbol, ANSIColors.RESET)

    def colorize_board(self, board: str) -> str:
        """Apply ANSI colors to the board display"""
        colored_board = board
        for symbol, colored_symbol in self.color_map.items():
            colored_board = colored_board.replace(f" {symbol}", f" {colored_symbol}")
        return colored_board


class ANSIVisualizer(BaseVisualizer):
    """ANSI terminal-based visualizer for ColorTile game"""

    def __init__(self, game):
        super().__init__(game)
        self.delay = 0.1
        self.ansi_colors = ANSIColors()
        self.current_click_position = None

    def get_board_str(self) -> str:
        """Return a plain text representation of the board"""
        lines = []
        lines.append(f"Score: {self.game.get_score()}")
        lines.append("   " + "".join(f"{i:2}" for i in range(self.game.board.WIDTH)))

        for row in range(self.game.board.HEIGHT):
            line = f"{row:2} "
            for col in range(self.game.board.WIDTH):
                tile = self.game.board.get_tile(row, col)
                if (
                    self.current_click_position
                    and (row, col) == self.current_click_position
                ):
                    line += " X"
                elif tile is None:
                    line += " ."
                else:
                    line += f" {tile.get_color_symbol()}"
            lines.append(line)

        res = "\n".join(lines)
        return self.ansi_colors.colorize_board(res)

    def display_frame(self) -> None:
        """Display a single frame of the animation with ANSI colors"""
        print(f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_CYAN}{'=' * 60}{ANSIColors.RESET}")

        board_str = self.get_board_str()
        print(board_str + "\n")

        remaining_info = f"{ANSIColors.BRIGHT_MAGENTA}Remaining tiles: {self.game.get_remaining_tiles()}{ANSIColors.RESET}"
        print(remaining_info)
        print(f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_CYAN}{'=' * 60}{ANSIColors.RESET}")

    def animate_solution(self, answer: Answer) -> Any:
        """Animate the solution step by step with reduced timing"""

        # Show initial state
        self.current_click_position = None
        self.display_frame()
        time.sleep(0.1)

        # Animate each move
        for i, move in enumerate(answer.moves, 1):
            # Apply the move
            self.game.click(move.row, move.col)

            # Set the clicked position for display
            self.current_click_position = (move.row, move.col)

            self.display_frame()
            time.sleep(0.1)

        # Show final summary with colors
        final_header = (
            f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_GREEN}{'=' * 60}{ANSIColors.RESET}"
        )
        final_title = f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_WHITE}GAME ANALYSIS COMPLETE{ANSIColors.RESET}"
        print(final_header)
        print(final_title)
        print(final_header)

        return None
