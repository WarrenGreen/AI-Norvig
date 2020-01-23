from ai.learning.reinforcement.active.q_learning_agent import train
from ai.problem.grid_leaky_transition_model import GridLeakyTransitionModelProblem

problem = GridLeakyTransitionModelProblem.create_start()
train(problem)
