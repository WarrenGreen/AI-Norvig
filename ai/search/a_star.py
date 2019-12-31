from queue import PriorityQueue

from ai.search.exception import InputException, NoValidPathException


def search(initial_state, goal_state, heuristic_fn):
    """

    Args:
        initial_state (GraphNode):
        goal_state (GraphNode):
        heuristic_fn (Callable[GraphNode, GraphNode]): function to estimate cost between parameter
            node and goal state

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    if initial_state is None or goal_state is None:
        raise InputException("Initial state and goal state cannot be None.")

    explored = {initial_state}
    frontier = PriorityQueue()
    frontier.put((0, initial_state, []))
    frontier_set = {initial_state: 999999}
    while not frontier.empty():
        path_cost, node, path = frontier.get_nowait()
        explored.add(node)
        new_path = path + [node]
        if node == goal_state:
            return new_path
        for edge_cost, child_node in node.edges:
            child_cost = path_cost + edge_cost + heuristic_fn(child_node, goal_state)
            if (child_node not in explored and child_node not in frontier_set) or (
                child_node in frontier_set and frontier_set[child_node] > child_cost
            ):
                frontier.put((child_cost, child_node, new_path))
                frontier_set[child_node] = child_cost

    raise NoValidPathException("No valid path between initial state and goal state.")
