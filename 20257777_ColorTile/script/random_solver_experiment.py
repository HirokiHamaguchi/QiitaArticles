"""
Random Solver Performance Experiment

This script tests RandomSolver performance across different seeds (0-99)
and creates a histogram of remaining tiles.
"""

import matplotlib.pyplot as plt
import numpy as np

from src.base.game import Game
from src.solver import RandomSolver


def run_random_solver_experiment(num_seeds=100):
    """Run RandomSolver with seeds 0 to num_seeds-1 and collect remaining tiles."""
    remaining_tiles = []

    for seed in range(num_seeds):
        # Create fresh game for each run
        game = Game(seed)
        solver = RandomSolver(game, seed=seed)

        # Solve the game
        solver.solve(max_moves=200)

        # Record remaining tiles
        tiles_left = game.get_remaining_tiles()
        remaining_tiles.append(tiles_left)

        if seed % 10 == 0:
            print(f"Seed {seed}: {tiles_left} tiles remaining")

    return remaining_tiles


def create_histogram(remaining_tiles, output_path):
    """Create and save histogram of remaining tiles."""
    plt.figure(figsize=(10, 6))

    # Create histogram
    plt.hist(remaining_tiles, bins=20, alpha=0.7, color="skyblue", edgecolor="black")

    # Add statistics
    mean_tiles = np.mean(remaining_tiles)
    median_tiles = np.median(remaining_tiles)
    min_tiles = np.min(remaining_tiles)
    max_tiles = np.max(remaining_tiles)

    plt.axvline(
        mean_tiles, color="red", linestyle="--", label=f"Mean: {mean_tiles:.1f}"
    )
    plt.axvline(
        median_tiles,
        color="orange",
        linestyle="--",
        label=f"Median: {median_tiles:.1f}",
    )

    plt.xlabel("Remaining Tiles")
    plt.ylabel("Frequency")
    plt.title("RandomSolver Performance Distribution (Seeds 0-99)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add text box with statistics
    stats_text = f"Min: {min_tiles}\nMax: {max_tiles}\nMean: {mean_tiles:.1f}\nMedian: {median_tiles:.1f}"
    plt.text(
        0.02,
        0.98,
        stats_text,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    return {
        "mean": mean_tiles,
        "median": median_tiles,
        "min": min_tiles,
        "max": max_tiles,
        "std": np.std(remaining_tiles),
    }


def main():
    print("Starting RandomSolver experiment...")
    print("Testing seeds 0-99...")

    # Run experiment
    remaining_tiles = run_random_solver_experiment(100)

    # Create histogram
    output_path = "imgs/experiments/random_solver_performance.png"
    stats = create_histogram(remaining_tiles, output_path)

    print("\nExperiment completed!")
    print(f"Results saved to: {output_path}")
    print("\nStatistics:")
    print(f"  Mean remaining tiles: {stats['mean']:.2f}")
    print(f"  Median remaining tiles: {stats['median']:.2f}")
    print(f"  Min remaining tiles: {stats['min']}")
    print(f"  Max remaining tiles: {stats['max']}")
    print(f"  Standard deviation: {stats['std']:.2f}")


if __name__ == "__main__":
    main()
