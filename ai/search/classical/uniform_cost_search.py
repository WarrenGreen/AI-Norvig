from queue import PriorityQueue

from ai.search.exception import NoValidPathException
from ai.problem import GraphProblem


def search(problem: GraphProblem):
    """

    Args:
        problem (GraphProblem):

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    current_state = problem.start_node

    explored = {current_state}
    frontier = PriorityQueue()
    frontier.put((0, current_state, []))
    frontier_set = {current_state: 999999}
    while not frontier.empty():
        path_cost, node, path = frontier.get_nowait()
        explored.add(node)
        new_path = path + [node]
        if problem.is_terminal(node):
            return new_path
        for edge_cost, child_node in problem.generate_successors(node):
            child_cost = path_cost + edge_cost
            if (child_node not in explored and child_node not in frontier_set) or (
                child_node in frontier_set and frontier_set[child_node] > child_cost
            ):
                frontier.put((child_cost, child_node, new_path))
                frontier_set[child_node] = child_cost

    raise NoValidPathException("No valid path between initial state and goal state.")
