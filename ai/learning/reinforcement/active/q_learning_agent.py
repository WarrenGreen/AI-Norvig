from collections import defaultdict

from ai.learning.learning_rate_schedules import scaled_learning_rate
from ai.learning.reinforcement.active.util import exploration_function
from ai.problem.grid import GridProblem


def train(
    problem: GridProblem = GridProblem.create_start(),
    epochs=1000,
    gamma=1.0,
    learning_rate_fn=None,
    frequency_cutoff=3,
    print_logs=True,
):
    if learning_rate_fn is None:
        learning_rate_fn = scaled_learning_rate(epochs)

    state_action_frequency = defaultdict(lambda: 0)  # N[s,a]
    action_utility = defaultdict(lambda: 0)  # Q-table
    exploration_fn = exploration_function(frequency_cutoff)
    for epoch in range(1, epochs + 1):
        path = []
        previous_state = None
        current_state = problem.start_location
        previous_action = None
        previous_reward = 0.0
        while True:
            if problem.is_terminal(current_state):
                action_utility[(previous_state, previous_action)] = problem.get_value(
                    current_state
                )
            path.append(current_state)
            state_action_frequency[(previous_state, previous_action)] += 1
            max_action_delta = None
            for action in problem.generate_actions(current_state):
                action_delta = (
                    action_utility[(current_state, action)]
                    - action_utility[(previous_state, previous_action)]
                )
                if max_action_delta is None or max_action_delta < action_delta:
                    max_action_delta = action_delta

            action_utility[(previous_state, previous_action)] += learning_rate_fn(
                epoch
            ) * (previous_reward + gamma * max_action_delta)

            if problem.is_terminal(current_state):
                break
            previous_state = current_state
            max_action_utility = None
            max_action = None
            for action in problem.generate_actions(current_state):
                utility = exploration_fn(
                    action_utility[(current_state, action)],
                    state_action_frequency[(current_state, action)],
                )
                if max_action_utility is None or max_action_utility < utility:
                    max_action_utility = utility
                    max_action = action
            previous_action = max_action
            previous_reward = problem.get_value(current_state)
            current_state = problem.apply_action(current_state, previous_action)

        if print_logs:
            print(f"Epoch {epoch}")
            problem.visualize(path)
            print()
            print()
            print()
