"""
Base visualizer class for ColorTile game
"""

from abc import ABC, abstractmethod
from typing import Any

from src.base.answer import Answer
from src.base.game import Game


class BaseVisualizer(ABC):
    """Abstract base class for all visualizers"""

    def __init__(self, game: Game):
        self.game = game

    @abstractmethod
    def display_frame(self) -> None:
        """Display a single frame of the animation"""
        pass

    @abstractmethod
    def animate_solution(self, answer: Answer) -> Any:
        """Animate the solution step by step"""
        pass

    def get_remaining_tiles(self) -> int:
        """Get the number of remaining tiles on the board"""
        return self.game.get_remaining_tiles()

    def get_score(self) -> int:
        """Get the current score"""
        return self.game.get_score()
