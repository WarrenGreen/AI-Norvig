from collections import defaultdict

from ai.learning.reinforcement.policy.maximum_policy import MaximumPolicy
from ai.problem.grid import GridProblem


def train(
    problem: GridProblem = GridProblem.create_start(), policy=MaximumPolicy, epochs=100, gamma=1.0, print_logs=True
):
    rewards = {}
    utilities = {}
    transition_frequency = defaultdict(lambda: defaultdict(lambda: 0))  # N[s`|s,a]
    action_frequency = defaultdict(lambda: 0)  # N[s,a]

    for epoch in range(1, epochs+1):
        previous_state, applied_action = None, None
        current_state = problem.start_location
        path = []
        while True:
            path.append(current_state)
            if current_state not in utilities:
                utilities[current_state] = problem.get_value(current_state)
                rewards[current_state] = problem.get_value(current_state)

            transition_frequency[current_state][(previous_state, applied_action)] += 1
            action_frequency[(previous_state, applied_action)] += 1

            new_utilities = {}
            for state in transition_frequency.keys():
                summed_previous_state_utility = 0.0
                for state_action, frequency in transition_frequency[state].items():
                    summed_previous_state_utility += (frequency / action_frequency[state_action]) * utilities[state]
                new_utilities[state] = min(max(rewards[state] + gamma * summed_previous_state_utility, -10), 10)  # Bound utility estimation to prevent overflow
            utilities = new_utilities

            if problem.is_terminal(current_state):
                break

            previous_state = current_state
            possible_actions = []
            for action in problem.generate_actions(current_state):
                row_delta, col_delta = action
                row, col = current_state
                action_state = row+row_delta, col+col_delta
                utility = 0.0
                if action_state in utilities:
                    utility = utilities[action_state]
                possible_actions.append((action, utility))

            previous_action = policy.get_next_move(possible_actions)
            current_state = problem.apply_action(current_state, previous_action)

        if print_logs:
            print(f"Epoch {epoch}")
            problem.visualize(path)
            print()
            print()
            print()

    return utilities
