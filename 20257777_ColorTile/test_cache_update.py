#!/usr/bin/env python3
"""
Test script to verify cache update functionality
"""

from src.base.game import Game
from src.solver.greedy_solver import GreedySolver


def test_cache_update():
    """Test if cache update works correctly"""
    game = Game(seed=42)
    solver = GreedySolver(game)

    print("Testing cache update functionality...")

    # Get initial valid moves
    valid_moves1 = solver._find_all_valid_moves()
    print(f"Initial valid moves count: {len(valid_moves1)}")

    if valid_moves1:
        # Make a move
        row, col, expected_points = valid_moves1[0]
        print(f"Making move at ({row}, {col}), expected points: {expected_points}")

        # Get removable tiles before clicking for verification
        removable_before = game.board.find_removable_tiles(row, col)
        print(f"Removable tiles before click: {len(removable_before)}")

        # Use the cache update method
        actual_points = solver.click_with_cache_update(row, col)
        print(f"Actual points: {actual_points}")

        # Check if points match
        if actual_points == expected_points:
            print("✓ Points match!")
        else:
            print(
                f"✗ Points don't match: expected {expected_points}, got {actual_points}"
            )
            return False

        # Get valid moves after the click
        valid_moves2 = solver._find_all_valid_moves()
        print(f"Valid moves after click: {len(valid_moves2)}")

        print("✓ Cache update test completed successfully")
        return True
    else:
        print("No valid moves found")
        return False


if __name__ == "__main__":
    test_cache_update()
