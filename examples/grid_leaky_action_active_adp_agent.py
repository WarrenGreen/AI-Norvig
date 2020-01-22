from ai.learning.reinforcement.passive.adp_agent import train
from ai.learning.reinforcement.policy.maximum_policy_with_random_exploration import \
    MaximumPolicyRandomExploration
from ai.problem.grid_leaky_transition_model import GridLeakyTransitionModelProblem

problem = GridLeakyTransitionModelProblem.create_start()
train(problem, MaximumPolicyRandomExploration)
