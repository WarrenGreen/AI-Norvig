import argparse

from ai.search.adversarial.minimax import search as search_minimax
from ai.search.adversarial.alpha_beta import search as search_alpha_beta
from ai.search.problem.chess import Chess


def main(config):
    problem = Chess()
    state = problem.create_start()
    while not problem.is_terminal(state):
        if config.alpha_beta:
            new_state, new_value = search_alpha_beta(
                problem, state, max_depth=config.depth
            )
        else:
            new_state, new_value = search_minimax(
                problem, state, maxthon_depth=config.depth
            )
        state = new_state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Have two chess agents play each other."
    )
    parser.add_argument(
        "--alpha_beta", action="store_true", help="Use Alpha-Beta",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=None,
        help="Maximum number of plys for each agent to search.",
    )
    main(parser.parse_args())
