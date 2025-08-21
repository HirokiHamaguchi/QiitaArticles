"""
Find All Clear - Seed Search for Complete Solutions

This script searches for seeds that result in completely clearing the board
(remaining tiles = 0) using RandomSolver and GreedySolver, then visualizes the solutions as GIFs.
"""

import os
from typing import List, Tuple

from src.base.answer import Answer
from src.base.game import Game
from src.solver import GreedySolver, RandomSolver
from src.vis.plt import MatplotlibVisualizer


def find_all_clear_seeds(
    max_seeds: int = 1000, max_moves: int = 200
) -> List[Tuple[int, Game, Answer, str]]:
    """
    Search for seeds that result in completely clearing the board using both RandomSolver and GreedySolver.

    Args:
        max_seeds: Maximum number of seeds to test
        max_moves: Maximum moves per solver attempt

    Returns:
        List of tuples containing (seed, game_state, answer, solver_type) for successful clears
    """
    successful_seeds = []

    print(
        f"Searching for seeds that clear all tiles using both RandomSolver and GreedySolver (testing up to {max_seeds} seeds)..."
    )

    for seed in range(max_seeds):
        # Test RandomSolver
        game = Game(seed)
        solver = RandomSolver(game, seed=seed)
        answer = solver.solve(max_moves=max_moves)
        tiles_left = game.get_remaining_tiles()

        if tiles_left == 0:
            print(
                f"SUCCESS! RandomSolver with seed {seed}: All tiles cleared in {len(answer.moves)} moves"
            )
            game.reset()
            successful_seeds.append((seed, game, answer, "random"))

        # Test GreedySolver
        game = Game(seed)
        solver2 = GreedySolver(game)
        answer = solver2.solve(max_moves=max_moves)
        tiles_left = game.get_remaining_tiles()

        if tiles_left == 0:
            print(
                f"SUCCESS! GreedySolver with seed {seed}: All tiles cleared in {len(answer.moves)} moves"
            )
            game.reset()
            successful_seeds.append((seed, game, answer, "greedy"))

        if seed % 10 == 0:
            print(f"Tested seed {seed}")

        # Stop after finding at least one successful solution for each solver type
        if len(successful_seeds) >= 2:
            has_random = any(
                solver_type == "random" for _, _, _, solver_type in successful_seeds
            )
            has_greedy = any(
                solver_type == "greedy" for _, _, _, solver_type in successful_seeds
            )
            if has_random and has_greedy:
                break

    return successful_seeds


def visualize_solution(
    seed: int,
    game: Game,
    answer: Answer,
    solver_type: str,
    output_dir: str = "imgs/all_clear",
) -> None:
    """
    Visualize the solution and save as GIF.

    Args:
        seed: The seed used for the solution
        game: Game instance (should be reset to initial state)
        answer: Answer object containing the solution moves
        solver_type: Type of solver used ("random" or "greedy")
        output_dir: Directory to save the visualization
    """
    print(f"\nCreating visualization for {solver_type} solver with seed {seed}...")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create visualizer with matplotlib backend for GIF creation
    visualizer = MatplotlibVisualizer(game)

    # Create the animation and save as GIF with custom path
    gif_path = os.path.join(output_dir, f"animation_{solver_type}_seed{seed}.gif")
    print(f"Generating animation and saving to {gif_path}...")
    anim = visualizer.animate_solution(answer, save_gif=True, gif_path=gif_path)

    if anim is not None:
        print(f"✓ Animation saved to {gif_path}")
    else:
        print("✗ Failed to create animation")


def main():
    """Main function to find all-clear seeds and visualize them."""
    print("=" * 60)
    print("Find All Clear - ColorTile Complete Solution Finder")
    print("=" * 60)

    # Search for seeds that clear all tiles
    successful_seeds = find_all_clear_seeds(max_seeds=1000, max_moves=200)

    if not successful_seeds:
        print("\n❌ No seeds found that clear all tiles within the search range.")
        print("Try increasing max_seeds or max_moves parameters.")
        return

    print(f"\n✅ Found {len(successful_seeds)} successful seed(s)!")

    # Visualize each successful solution
    for seed, game, answer, solver_type in successful_seeds:
        visualize_solution(seed, game, answer, solver_type)


if __name__ == "__main__":
    main()
