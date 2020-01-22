from collections import defaultdict

from ai.learning.reinforcement.policy.maximum_policy import MaximumPolicy
from ai.problem.grid import GridProblem


def scaled_learning_rate(total_epochs):
    def learning_rate(epoch):
        return total_epochs / (total_epochs + epoch)

    return learning_rate


def train(
    problem: GridProblem = GridProblem.create_start(),
    policy=MaximumPolicy,
    epochs=100,
    gamma=1.0,
    learning_rate_fn=None,
    print_logs=True,
):
    if learning_rate_fn is None:
        learning_rate_fn = scaled_learning_rate(epochs)
    rewards = {None: 0.0}
    utilities = {None: 0.0}

    for epoch in range(1, epochs + 1):
        previous_state, applied_action, previous_reward = None, None, 0.0
        current_state = problem.start_location
        path = []
        while True:
            path.append(current_state)
            if current_state not in utilities:
                utilities[current_state] = problem.get_value(current_state)
                rewards[current_state] = problem.get_value(current_state)

            utilities[previous_state] += rewards[previous_state] + learning_rate_fn(epoch) * (previous_reward + gamma * utilities[current_state] - utilities[previous_state])

            if problem.is_terminal(current_state):
                break

            possible_actions = []
            for action in problem.generate_actions(current_state):
                row_delta, col_delta = action
                row, col = current_state
                action_state = row + row_delta, col + col_delta
                utility = 0.0
                if action_state in utilities:
                    utility = utilities[action_state]
                possible_actions.append((action, utility))

            previous_state = current_state
            previous_action = policy.get_next_move(possible_actions)
            current_state = problem.apply_action(current_state, previous_action)

        if print_logs:
            print(f"Epoch {epoch}")
            problem.visualize(path)
            print()
            print()
            print()

    return utilities
