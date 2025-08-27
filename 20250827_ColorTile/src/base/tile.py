"""
Tile class for ColorTile game
"""

from enum import Enum


class TileColor(Enum):
    """Enum representing the 10 different tile colors"""

    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    PURPLE = 5
    ORANGE = 6
    PINK = 7
    CYAN = 8
    BROWN = 9
    GRAY = 10


class Tile:
    """Represents a single tile in the game"""

    def __init__(self, color: TileColor):
        self.color = color

    def __str__(self):
        return f"Tile({self.color.name})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.color == other.color
        return False

    def get_color_symbol(self) -> str:
        """Returns a single character symbol for the tile color"""
        symbols = {
            TileColor.RED: "R",
            TileColor.BLUE: "B",
            TileColor.GREEN: "G",
            TileColor.YELLOW: "Y",
            TileColor.PURPLE: "P",
            TileColor.ORANGE: "O",
            TileColor.PINK: "K",
            TileColor.CYAN: "C",
            TileColor.BROWN: "N",
            TileColor.GRAY: "A",
        }
        return symbols[self.color]
