from collections import defaultdict

from ai.learning.reinforcement.active.util import exploration_function
from ai.problem.grid import GridProblem


def train(
    problem: GridProblem = GridProblem.create_start(),
    frequency_cutoff=3,
    epochs=100,
    gamma=1.0,
    print_logs=True,
):
    exploration_fn = exploration_function(frequency_cutoff)
    utilities = {}
    transition_frequency = defaultdict(lambda: defaultdict(lambda: 0))  # N[s`|s,a]
    action_frequency = defaultdict(lambda: 0.00001)  # N[s,a]

    for epoch in range(1, epochs + 1):
        previous_state, applied_action = (0, 0), (0, 0)
        current_state = problem.start_location
        path = []
        while True:
            path.append(current_state)
            if current_state not in utilities:
                utilities[current_state] = problem.get_value(current_state)

            transition_frequency[current_state][(previous_state, applied_action)] += 1
            action_frequency[(previous_state, applied_action)] += 1

            possible_actions = []
            max_action = None
            max_action_utility = None
            for action in problem.generate_actions(current_state):
                new_state = problem.apply_action(current_state, action)
                utility = 0.0
                if new_state in utilities:
                    utility = utilities[new_state]

                utility *= (
                    transition_frequency[new_state][(current_state, action)]
                    / action_frequency[(current_state, action)]
                )
                utility = exploration_fn(
                    utility, action_frequency[(current_state, action)]
                )
                if max_action_utility is None or utility > max_action_utility:
                    max_action = action
                    max_action_utility = utility
                possible_actions.append((action, utility))

            utilities[current_state] = (
                problem.get_value(current_state) + gamma * max_action_utility
            )

            if problem.is_terminal(current_state):
                break
            previous_state = current_state
            applied_action = max_action
            current_state = problem.apply_action(current_state, applied_action)

        if print_logs:
            print(f"Epoch {epoch}")
            problem.visualize(path)
            print()
            print()
            print()

    return utilities
