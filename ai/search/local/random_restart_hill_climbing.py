from ai.search.local.hill_climbing import search as hill_climb


def search(
    problem, goal=0, sideways_moves=False, successor_mode="steepest", max_attempts=None
):
    """
    Args:
        problem (Problem):
        goal (int): Goal value to reach
        sideways_moves (bool): Allow sideways moves on plateaus
        successor_mode (str): Which successor selection mode to choose.
                                ["steepest", "first-choice", "stochastic"]
        max_attempts (int): maximum number of attempts. `None` signifies infinite.

    Returns:
        Tuple[List, int] solution state and solution value
    """
    attempts = 0
    while max_attempts is None or attempts > max_attempts:
        attempts += 1
        result, result_value = hill_climb(problem, sideways_moves, successor_mode)
        if result_value == goal:
            return result, result_value
