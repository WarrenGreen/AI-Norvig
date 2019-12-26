def search(initial_state, goal_state, limit=None):
    """
        Low-memory depth-first implementation.

        Args:
            initial_state (GraphNode):
            goal_state (GraphNode):
            limit (Optional[int]): Maximum depth to traverse. `None` value
                signifies infinite depth.

        Returns:
            List[GraphNode] - optimal path from initial_state to goal_state
        """
    path = _search(initial_state, goal_state, limit)
    if path is None:
        raise ValueError("No valid path between initial state and goal state.")
    return path


def _search(initial_state, goal_state, limit):
    if initial_state is None or goal_state is None:
        raise ValueError("No valid path between initial state and goal state.")

    if limit is not None:
        if limit <= 0:
            return None
        limit -= 1

    if initial_state == goal_state:
        return [goal_state]

    for _, child_node in initial_state.edges:
        path = _search(child_node, goal_state, limit)
        if path is not None:
            return [initial_state] + path

    return None
