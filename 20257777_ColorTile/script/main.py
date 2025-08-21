"""
ColorTile Game Analysis Demo
"""

import threading

from src.base.board import BoardType
from src.base.game import Game
from src.solver import GreedySolver, RandomSolver
from src.vis.ansi import ANSIVisualizer
from src.vis.plt import MatplotlibVisualizer


def timeout_input(prompt, timeout=5, default=""):
    """Get user input with timeout. Returns default value if timeout occurs."""
    result = [default]  # Use list to modify from inner function

    def get_input():
        try:
            result[0] = input(prompt)
        except EOFError:
            pass

    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)

    if input_thread.is_alive():
        print(f"\nTimeout after {timeout} seconds. Using default: '{default}'")
        return default
    else:
        return result[0]


def main():
    # Choose board type
    print("Choose board type:")
    print("1. PC version (23x15, 10 tile types)")
    print("2. App version (10x13, 5 tile types)")
    print("3. Experiment version (5x6, 1 tile type)")

    board_choice = timeout_input(
        "Choose board type (1-3, default 2): ", timeout=5, default="2"
    ).strip()

    if board_choice == "1":
        board_type = BoardType.PC
        board_name = "pc"
        print("Using PC version board")
    elif board_choice == "3":
        board_type = BoardType.EXPERIMENT
        board_name = "experiment"
        print("Using Experiment version board")
    else:
        board_type = BoardType.APP
        board_name = "app"
        print("Using App version board")

    game = Game(seed=0, board_type=board_type)

    print("Initial game state:")
    # Use ANSI visualizer for initial display
    ansi_visualizer = ANSIVisualizer(game)
    print(ansi_visualizer.get_board_str())
    print(f"Initial tiles: {game.get_remaining_tiles()}")
    print()

    # Choose solver type
    print("Choose solver type:")
    print("1. Greedy Solver (selects moves with highest points)")
    print("2. Random Solver (selects moves randomly)")

    solver_choice = timeout_input(
        "Choose solver (1-2, default 1): ", timeout=5, default="1"
    ).strip()

    if solver_choice == "2":
        solver = RandomSolver(game, seed=42)  # Use seed for reproducible results
        solver_name = "random"
        print("Using Random Solver")
    else:
        solver = GreedySolver(game)
        solver_name = "greedy"
        print("Using Greedy Solver")

    answer = solver.solve(max_moves=100)
    print(f"Solution found with {len(answer.moves)} moves.")

    # Show visualization options
    print("\nVisualization options:")
    print("1. Terminal animation (ANSI colors)")
    print("2. Matplotlib static board (saves to imgs/static_board.png)")
    print("3. Matplotlib animation (saves to imgs/final_board.png)")
    print("4. Matplotlib animation with GIF (saves to imgs/animation.gif)")

    choice = timeout_input(
        "Choose visualization (1-4, default 1): ", timeout=5, default="1"
    ).strip()

    game.reset()

    if choice == "2":
        plt_visualizer = MatplotlibVisualizer(game)
        plt_visualizer.save_static_board(
            f"imgs/static_board_{board_name}_{solver_name}.png"
        )
    elif choice == "3":
        plt_visualizer = MatplotlibVisualizer(game)
        plt_visualizer.animate_solution(answer, save_gif=False)
    elif choice == "4":
        plt_visualizer = MatplotlibVisualizer(game)
        gif_path = f"imgs/animation_{board_name}_{solver_name}_demo.gif"
        plt_visualizer.animate_solution(answer, save_gif=True, gif_path=gif_path)
    else:
        # Default terminal animation
        ansi_visualizer = ANSIVisualizer(game)
        ansi_visualizer.animate_solution(answer)


if __name__ == "__main__":
    main()
