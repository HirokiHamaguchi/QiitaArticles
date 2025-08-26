"""
Matplotlib-based visualizer for ColorTile game
"""

import os
from typing import Any, Optional

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from src.base.answer import Answer
from src.base.game import Game
from src.base.tile import TileColor


class MatplotlibVisualizer:
    """Matplotlib-based visualizer for ColorTile game"""

    def __init__(self, game: Game) -> None:
        self.game = game

        # Color mapping for matplotlib visualization
        self.color_map = {
            TileColor.RED: "#FF0000",
            TileColor.BLUE: "#0000FF",
            TileColor.GREEN: "#00FF00",
            TileColor.YELLOW: "#FFFF00",
            TileColor.PURPLE: "#800080",
            TileColor.ORANGE: "#FFA500",
            TileColor.PINK: "#FFC0CB",
            TileColor.CYAN: "#00FFFF",
            TileColor.BROWN: "#8B4513",
            TileColor.GRAY: "#808080",
        }

        # Matplotlib animation properties
        self.fig: Optional[Any] = None
        self.ax: Optional[Any] = None
        self.im: Optional[Any] = None
        self.frames: list[dict[str, Any]] = []
        self.x_markers: list[Any] = []  # Store X markers for clicked positions
        self.fade_rectangles: list[Any] = []  # Store fade overlay rectangles

        # Set matplotlib to non-interactive mode
        plt.ioff()

    def get_board_matrix(self) -> np.ndarray:
        """Convert board to a numerical matrix for matplotlib visualization"""
        matrix = np.zeros((self.game.board.HEIGHT, self.game.board.WIDTH))

        for row in range(self.game.board.HEIGHT):
            for col in range(self.game.board.WIDTH):
                tile = self.game.board.get_tile(row, col)
                if tile is not None:
                    matrix[row, col] = tile.color.value
                else:
                    matrix[row, col] = 0  # Empty cell

        return matrix

    def create_color_matrix(self) -> np.ndarray:
        """Create RGB color matrix for visualization"""
        board_matrix = self.get_board_matrix()
        height, width = board_matrix.shape
        color_matrix = np.zeros((height, width, 3))

        for row in range(height):
            for col in range(width):
                tile_value = int(board_matrix[row, col])
                if tile_value == 0:  # Empty cell
                    color_matrix[row, col] = [1.0, 1.0, 1.0]
                else:
                    color = list(TileColor)[tile_value - 1]
                    hex_color = self.color_map[color]
                    # Convert hex to RGB (0-1 range)
                    r = int(hex_color[1:3], 16) / 255.0
                    g = int(hex_color[3:5], 16) / 255.0
                    b = int(hex_color[5:7], 16) / 255.0

                    # Use the original colors without fading
                    color_matrix[row, col] = [r, g, b]

        return color_matrix

    def setup_matplotlib_figure(self):
        """Setup matplotlib figure for animation"""
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_title("ColorTile Game Animation", fontsize=16, fontweight="bold")
        self.ax.set_aspect("equal")

        # Remove axis ticks and labels for cleaner look
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Initialize with current board state
        color_matrix = self.create_color_matrix()
        self.im = self.ax.imshow(color_matrix, aspect="equal")

        # Add score text
        self.score_text = self.ax.text(
            0.02,
            0.98,
            f"Score: {self.game.get_score()}",
            transform=self.ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

        plt.tight_layout()

    def draw_x_markers(self, click_position):
        """Draw red X markers on the clicked position"""
        if self.ax is None:
            return

        # Clear previous X markers
        for marker in self.x_markers:
            marker.remove()
        self.x_markers.clear()

        # Draw X marker for the clicked position (if provided)
        if click_position is not None:
            row, col = click_position
            # Draw X marker at the clicked position
            x_marker = self.ax.text(
                col,
                row,
                "✗",
                ha="center",
                va="center",
                fontsize=20,
                fontweight="bold",
                color="red",
                bbox=dict(boxstyle="round,pad=0.1", facecolor="white", alpha=0.8),
            )
            self.x_markers.append(x_marker)

    def draw_fade_rectangles(self, tiles_to_fade):
        """Draw semi-transparent rectangle overlays on tiles that will be removed"""
        if self.ax is None:
            return

        # Clear previous fade rectangles
        for rect in self.fade_rectangles:
            rect.remove()
        self.fade_rectangles.clear()

        # Draw fade rectangles for tiles that will be removed
        if tiles_to_fade:
            for row, col in tiles_to_fade:
                fade_rect = Rectangle(
                    (col - 0.5, row - 0.5),  # Bottom-left corner
                    1.0,  # Width
                    1.0,  # Height
                    facecolor="none",
                    edgecolor="black",
                    linewidth=5,
                )
                self.ax.add_patch(fade_rect)
                self.fade_rectangles.append(fade_rect)

    def capture_frame(self, click_position=None, tiles_to_remove=None):
        """Capture current game state as a frame"""
        frame = {
            "matrix": self.create_color_matrix(),
            "score": self.game.get_score(),
            "remaining": self.game.get_remaining_tiles(),
            "click_position": click_position,  # Store the clicked position
            "tiles_to_remove": tiles_to_remove,  # Store tiles that will be removed
        }
        self.frames.append(frame)

    def animate_solution(
        self, answer: Answer, save_gif: bool = False, gif_path: Optional[str] = None
    ) -> Any:
        """Animate the solution using matplotlib and save images

        Args:
            answer: The solution to animate
            save_gif: Whether to save the animation as a GIF
            gif_path: Custom path for the GIF file (if None, uses default "imgs/animation.gif")
        """
        try:
            # Reset frames
            self.frames = []

            # Capture initial state (no click position)
            self.capture_frame()

            # Apply each move and capture frames
            for move in answer.moves:
                # Before applying the move, find which tiles will be removed
                tiles_to_remove = self.game.preview_click(move.row, move.col)

                # Capture frame BEFORE the move, showing:
                # 1. Current board state with tiles that will be removed faded
                # 2. X marker on the click position
                self.frames.append(
                    {
                        "matrix": self.create_color_matrix(),
                        "score": self.game.get_score(),
                        "remaining": self.game.get_remaining_tiles(),
                        "click_position": (move.row, move.col),  # Show X marker
                        "tiles_to_remove": set(tiles_to_remove),
                    }
                )

                # Now apply the move
                self.game.click(move.row, move.col)

            # Setup matplotlib figure
            self.setup_matplotlib_figure()

            def animate_func(frame_num):
                """Animation function for matplotlib"""
                if frame_num < len(self.frames):
                    frame = self.frames[frame_num]
                    if self.im is not None:
                        self.im.set_array(frame["matrix"])
                    if hasattr(self, "score_text"):
                        self.score_text.set_text(f"Score: {frame['score']}")

                    # Draw X marker for the clicked position
                    self.draw_x_markers(frame["click_position"])

                    # Draw fade rectangles for tiles that will be removed
                    self.draw_fade_rectangles(frame.get("tiles_to_remove", None))

                    # Add move indicator
                    if frame_num > 0 and self.ax is not None:
                        move = answer.moves[frame_num - 1]
                        self.ax.set_title(
                            f"ColorTile Game Animation - Move {frame_num:>3}: ({move.row:>2}, {move.col:>2})",
                            fontsize=16,
                            fontweight="bold",
                            fontname="monospace",
                        )
                    elif self.ax is not None:
                        self.ax.set_title(
                            "ColorTile Game Animation - Initial State",
                            fontsize=16,
                            fontweight="bold",
                            fontname="monospace",
                        )

                return_list = []
                if self.im is not None:
                    return_list.append(self.im)
                if hasattr(self, "score_text"):
                    return_list.append(self.score_text)
                return_list.extend(self.x_markers)
                return_list.extend(self.fade_rectangles)
                return return_list

            # Create animation
            if self.fig is not None:
                anim = animation.FuncAnimation(
                    self.fig,
                    animate_func,
                    frames=len(self.frames),
                    interval=267,  # Reduced from 800 to 267 for 3x speed (800/3 ≈ 267)
                    blit=False,
                    repeat=True,
                )

                # Save as GIF if requested
                if save_gif:
                    if gif_path is not None:
                        gif_output_path = gif_path
                    else:
                        gif_output_path = os.path.join("imgs", "animation.gif")

                    print(f"Saving animation as {gif_output_path}...")
                    try:
                        # Ensure the directory exists
                        os.makedirs(os.path.dirname(gif_output_path), exist_ok=True)
                        anim.save(
                            gif_output_path, writer="pillow", fps=3
                        )  # Increased from 1 to 3 for 3x speed
                        print(f"Animation saved as {gif_output_path}")
                    except Exception as e:
                        print(f"Error saving animation: {e}")

                return anim
            else:
                print("Error: Figure not initialized properly")
                return None

        except Exception as e:
            print(f"Error creating matplotlib animation: {e}")
            return None
