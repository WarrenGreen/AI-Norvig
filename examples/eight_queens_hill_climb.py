import argparse

from ai.search.local.hill_climbing import search
from ai.search.local.problem import EightQueens


def main(config):
    problem = EightQueens(size=config.size)
    print(search(problem, sideways_moves=config.allow_sideways_moves))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run hill climber solver on eight queens."
    )
    parser.add_argument(
        "--size", type=int, default=8, help="Size of queens board square",
    )
    parser.add_argument(
        "--allow_sideways_moves",
        action="store_true",
        help="Allow sideways moves on plateaus",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="steepest",
        help="Successor strategy to use",
        choices=["steepest", "first-choice", "stochastic"],
    )

    main(parser.parse_args())
