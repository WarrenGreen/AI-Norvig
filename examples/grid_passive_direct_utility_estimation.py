from ai.learning.reinforcement.passive.direct_utility_estimation import (
    train,
    MaximumPolicy,
)
from ai.problem.grid import GridProblem

problem = GridProblem.create_start()
train(problem, MaximumPolicy)
