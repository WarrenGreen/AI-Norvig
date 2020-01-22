from collections import defaultdict

from ai.learning.reinforcement.policy.maximum_policy import MaximumPolicy
from ai.problem.grid import GridProblem


def train(
    problem: GridProblem = GridProblem.create_start(), policy=MaximumPolicy, epochs=15
):
    """
    Yields the following result using the default configs.

    Initial Grid
    |      -0.04 |      -0.04 |      -0.04 |        1.0  |
    |      -0.04 | ========== |      -0.04 |       -1.0  |
    |      start |      -0.04 |      -0.04 |      -0.04  |

    Path Followed
    |          X |          X |          X |          X  |
    |          X | ========== |      -0.04 |       -1.0  |
    |          X |      -0.04 |      -0.04 |      -0.04  |
    """
    utility_table = defaultdict(lambda: [0.0, 0])
    for _ in range(epochs):
        current_state = problem.start_location
        value = 0.0
        path = [current_state]
        while not problem.is_terminal(current_state):
            utility_table[current_state][0] += problem.get_value(current_state)
            utility_table[current_state][1] += 1
            sum, count = utility_table[current_state]
            value += sum / count
            successors = []
            for successor in problem.generate_successors(current_state):
                sum, count = utility_table[successor]
                avg = sum / count if count > 0 else 0
                successors.append((successor, avg))
            current_state = policy.get_next_move(successors)
            path.append(current_state)
        utility_table[current_state][0] += problem.get_value(current_state)
        utility_table[current_state][1] += 1

    problem.visualize(path)
