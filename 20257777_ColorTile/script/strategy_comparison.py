import os
from collections import defaultdict
from typing import Dict, List, Tuple, Type

import matplotlib.pyplot as plt
import numpy as np

from src.base.analyzer import GameAnalyzer
from src.base.board import BoardType
from src.base.game import Game
from src.solver import (
    DiagonalSolver,
    HorizontalSolver,
    RandomSolver,
    VerticalSolver,
)
from src.solver.base_solver import BaseSolver
from src.vis.plt import MatplotlibVisualizer


class StrategyComparison:
    """Class to run comprehensive strategy comparison experiment"""

    def __init__(self, num_experiments: int, max_moves: int, save_gif: bool):
        self.num_experiments = num_experiments
        self.max_moves = max_moves
        self.results: Dict[str, List[Dict]] = {}
        self.has_saved_all_clear: Dict[str, bool] = defaultdict(bool)
        self.save_gif = save_gif

    def run_single_experiment(
        self,
        strategy_name: str,
        solver_class: Type[BaseSolver],
        solver_kwargs: Dict,
        seed: int,
    ) -> Dict:
        """Run a single experiment with given solver and return analysis"""
        game = Game(seed, board_type=BoardType.PC)

        # Handle RandomSolver seed parameter specially
        if solver_class == RandomSolver:
            solver_kwargs = solver_kwargs.copy()
            solver_kwargs["seed"] = seed

        solver = solver_class(game, **solver_kwargs)

        answer = solver.solve(max_moves=self.max_moves)

        analyzer = GameAnalyzer(game)
        analysis = analyzer.analyze_game_result()

        analysis.update(
            {
                "seed": seed,
                "num_moves": len(answer.moves),
                "solver_type": strategy_name,
                "avoid_triple": solver_kwargs.get("avoid_triple", False),
            }
        )

        visualizer = MatplotlibVisualizer(game)

        if self.save_gif:
            GIF_DIR = "imgs/strategy_gifs"

            if seed == 0:
                print("seed 0: saving example gif")
                gif_path = f"{GIF_DIR}/{strategy_name}_example.gif"
                visualizer.animate_solution(answer, save_gif=True, gif_path=gif_path)

            if (
                analysis["is_complete_clear"]
                and not self.has_saved_all_clear[strategy_name]
            ):
                print(f"seed {seed}: saving all-clear gif for {strategy_name}")
                gif_path = f"{GIF_DIR}/{strategy_name}_all_clear.gif"
                visualizer.animate_solution(answer, save_gif=True, gif_path=gif_path)
                self.has_saved_all_clear[strategy_name] = True

            if seed < 10:
                visualizer.save_last_state(
                    f"imgs/last_state/{strategy_name}_seed{seed}.png"
                )

        return analysis

    def run_all_experiments(self) -> None:
        """Run experiments for all 8 strategies"""
        strategies: List[Tuple[str, Type[BaseSolver], Dict]] = [
            ("Random", RandomSolver, {"avoid_triple": False}),
            ("Horizontal", HorizontalSolver, {"avoid_triple": False}),
            ("Vertical", VerticalSolver, {"avoid_triple": False}),
            ("Diagonal", DiagonalSolver, {"avoid_triple": False}),
            ("Random (Triple Avoid)", RandomSolver, {"avoid_triple": True}),
            ("Horizontal (Triple Avoid)", HorizontalSolver, {"avoid_triple": True}),
            ("Vertical (Triple Avoid)", VerticalSolver, {"avoid_triple": True}),
            ("Diagonal (Triple Avoid)", DiagonalSolver, {"avoid_triple": True}),
        ]

        for strategy_name, solver_class, solver_kwargs in strategies:
            print(f"Running {self.num_experiments} experiments for {strategy_name}...")

            results = []
            for seed in range(self.num_experiments):
                result = self.run_single_experiment(
                    strategy_name, solver_class, solver_kwargs, seed
                )
                results.append(result)

            self.results[strategy_name] = results

            print("    Done.")

    def analyze_results(self) -> Dict[str, Dict]:
        """Analyze and summarize results for all strategies"""
        summary = {}

        assert len(self.results) == 8, "Expected results for 8 strategies."
        for strategy_name, results in self.results.items():
            # Calculate basic statistics
            scores = [r["final_score"] for r in results]
            remaining_tiles = [r["total_remaining_tiles"] for r in results]
            all_clear_count = sum(1 for r in results if r["is_complete_clear"])

            # Failure type analysis (only for incomplete games)
            incomplete_results = [r for r in results if not r["is_complete_clear"]]
            failure_types: Dict[str, int] = defaultdict(int)

            for result in incomplete_results:
                if result["has_odd_parity_failure"]:
                    failure_types["odd_parity"] += 1
                elif result["has_adjacent_pairs"]:
                    failure_types["adjacent_pairs"] += 1
                elif result["has_placement_failure"]:
                    failure_types["placement_failure"] += 1
                else:
                    raise RuntimeError("Unexpected failure type encountered.")

            summary[strategy_name] = {
                "mean_score": np.mean(scores),
                "std_score": np.std(scores),
                "mean_remaining": np.mean(remaining_tiles),
                "std_remaining": np.std(remaining_tiles),
                "all_clear_rate": all_clear_count / self.num_experiments * 100,
                "all_clear_count": all_clear_count,
                "failure_breakdown": dict(failure_types),
                "failure_rates": {
                    k: v / len(incomplete_results) * 100 if incomplete_results else 0
                    for k, v in failure_types.items()
                },
            }

        return summary

    def create_visualizations(self, output_dir: str = "imgs/experiments") -> None:
        """Create visualizations for the comparison results"""
        os.makedirs(output_dir, exist_ok=True)
        summary = self.analyze_results()
        strategies = list(summary.keys())

        # Create score distribution histogram for all strategies
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        axes = axes.flatten()
        bins = np.arange(180, 201, 1)
        all_counts = []
        for _, results in self.results.items():
            scores = [r["final_score"] for r in results]
            counts, _ = np.histogram([s for s in scores if 180 <= s <= 200], bins=bins)
            all_counts.append(counts)
        max_height = max([c.max() for c in all_counts]) if all_counts else 1

        for i, (strategy_name, results) in enumerate(self.results.items()):
            scores = [r["final_score"] for r in results]
            filtered_scores = [s for s in scores if 180 <= s <= 200]
            axes[i].hist(filtered_scores, bins=bins, alpha=0.7, edgecolor="black")
            axes[i].set_title(f"{strategy_name}\nMean: {np.mean(filtered_scores):.1f}")
            axes[i].set_xlabel("Score")
            axes[i].set_ylabel("Frequency")
            axes[i].set_xlim(180, 200)
            axes[i].set_ylim(0, max_height + 1)
            axes[i].grid(True, alpha=0.3)
            axes[i].set_xticks(np.arange(180, 201, 5))
            axes[i].set_xticklabels([str(x) for x in np.arange(180, 201, 5)])
        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "score_distributions.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

        # Create all-clear rate comparison bar chart
        rates = [summary[s]["all_clear_rate"] for s in strategies]
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(strategies)), rates, alpha=0.7)
        plt.xlabel("Strategy")
        plt.ylabel("All-Clear Rate (%)")
        plt.title("All-Clear Achievement Rate by Strategy")
        plt.xticks(range(len(strategies)), strategies, rotation=45, ha="right")
        plt.grid(True, alpha=0.3)
        for bar, rate in zip(bars, rates):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{rate:.1f}%",
                ha="center",
                va="bottom",
            )
        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "all_clear_rates.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

        # Create stacked bar chart showing failure type breakdown
        failure_types = ["odd_parity", "placement_failure", "adjacent_pairs"]
        failure_data: Dict[str, List[float]] = {ft: [] for ft in failure_types}
        for strategy in strategies:
            rates = summary[strategy]["failure_rates"]
            assert isinstance(rates, dict)
            for ft in failure_types:
                failure_data[ft].append(rates.get(ft, 0))
        fig, ax = plt.subplots(figsize=(12, 6))
        bottom = np.zeros(len(strategies))
        colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
        for i, (failure_type, values) in enumerate(failure_data.items()):
            ax.bar(
                strategies,
                values,
                bottom=bottom,
                label=failure_type.replace("_", " ").title(),
                color=colors[i],
                alpha=0.8,
            )
            bottom += values
        ax.set_xlabel("Strategy")
        ax.set_ylabel("Failure Rate (%)")
        ax.set_title("Failure Type Breakdown by Strategy (Among Incomplete Games)")
        ax.legend()
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "failure_breakdown.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()


def main():
    experiment = StrategyComparison(num_experiments=100, max_moves=1000, save_gif=False)
    experiment.run_all_experiments()
    experiment.create_visualizations()


if __name__ == "__main__":
    main()
