from queue import PriorityQueue


def search(initial_state, goal_state):
    """

    Args:
        initial_state (GraphNode):
        goal_state (GraphNode):

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    if initial_state is None or goal_state is None:
        raise ValueError("No valid path between initial state and goal state.")

    frontier = PriorityQueue()
    frontier.put((0, initial_state, []))
    while not frontier.empty():
        path_cost, node, path = frontier.get_nowait()
        new_path = path + [node]
        if node == goal_state:
            return new_path

        for edge_cost, child_node in node.edges:
            frontier.put((path_cost + edge_cost, child_node, new_path))

    raise ValueError("No valid path between initial state and goal state.")