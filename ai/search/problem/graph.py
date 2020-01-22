from ai.search.exception import InputException
from ai.search.problem.node import GraphNode
from ai.search.problem.problem import Problem


class GraphProblem(Problem):
    def __init__(self, start_node, goal_node):
        if start_node is None or goal_node is None:
            raise InputException("Initial state and goal state cannot be None.")
        self.start_node = start_node
        self.goal_node = goal_node

    def generate_successors(self, state: GraphNode):
        for edge_cost, edge_node in state.edges:
            yield edge_cost, edge_node

    def is_terminal(self, state):
        return state == self.goal_node
