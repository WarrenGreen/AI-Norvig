import argparse

from ai.search.local.hill_climbing import search as hill_climb
from ai.search.local.random_restart_hill_climbing import (
    search as random_restart_hill_climbing,
)
from ai.search.local.problem import EightQueens


def main(config):
    problem = EightQueens(size=config.size)
    if config.random_restart:
        print(
            random_restart_hill_climbing(
                problem,
                goal=0,
                sideways_moves=config.allow_sideways_moves,
                successor_mode=config.mode,
            )
        )
    else:
        print(
            hill_climb(
                problem,
                sideways_moves=config.allow_sideways_moves,
                successor_mode=config.mode,
            )
        )


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
        "--random_restart",
        action="store_true",
        help="Random restart until goal is reached",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="steepest",
        help="Successor strategy to use",
        choices=["steepest", "first-choice", "stochastic"],
    )

    main(parser.parse_args())
