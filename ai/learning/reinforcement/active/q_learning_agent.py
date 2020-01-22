from ai.learning.reinforcement.policy.maximum_policy import MaximumPolicy
from ai.problem.grid import GridProblem


def train(
    problem: GridProblem = GridProblem.create_start(),
    policy=MaximumPolicy,
    epochs=100,
    gamma=1.0,
    print_logs=True,
):