from queue import PriorityQueue

from ai.search.exception import NoValidPathException


def search(problem, heuristic_fn):
    """

    Args:
        problem (GraphProblem):
        heuristic_fn (Callable[GraphNode, GraphNode]): function to estimate cost between parameter
            node and goal state

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    explored = {problem.start_node}
    frontier = PriorityQueue()
    frontier.put((0, problem.start_node, []))
    frontier_set = {problem.start_node: 999999}
    while not frontier.empty():
        path_cost, node, path = frontier.get_nowait()
        explored.add(node)
        new_path = path + [node]
        if problem.is_terminal(node):
            return new_path
        for edge_cost, child_node in node.edges:
            child_cost = (
                path_cost + edge_cost + heuristic_fn(child_node, problem.goal_node)
            )
            if (child_node not in explored and child_node not in frontier_set) or (
                child_node in frontier_set and frontier_set[child_node] > child_cost
            ):
                frontier.put((child_cost, child_node, new_path))
                frontier_set[child_node] = child_cost

    raise NoValidPathException("No valid path between initial state and goal state.")
