from ai.search.exception import InputException, NoValidPathException


def search(initial_state, goal_state):
    """

    Args:
        initial_state (GraphNode):
        goal_state (GraphNode):

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    if initial_state is None or goal_state is None:
        raise InputException("Initial state and goal state cannot be None.")

    queue_1 = [(initial_state, [])]
    queue_2 = []

    while len(queue_1) > 0:
        node, path = queue_1.pop(0)
        new_path = path + [node]
        if node == goal_state:
            return new_path

        for edge_cost, child_node in node.edges:
            queue_2.append((child_node, new_path))

        if len(queue_1) == 0:
            queue_1 = queue_2
            queue_2 = []

    raise NoValidPathException("No valid path between initial state and goal state.")
