from ai.learning.reinforcement.active.q_learning_agent import train
from ai.problem.grid import GridProblem

problem = GridProblem.create_start()
train(problem)
