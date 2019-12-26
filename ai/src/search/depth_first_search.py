def search(initial_state, goal_state):
    path = _search(initial_state, goal_state)
    if path is None:
        raise ValueError("No valid path between initial state and goal state.")
    return path


def _search(initial_state, goal_state):
    if initial_state is None or goal_state is None:
        raise ValueError("No valid path between initial state and goal state.")

    if initial_state == goal_state:
        return [goal_state]

    for _, child_node in initial_state.edges:
        path = _search(child_node, goal_state)
        if path is not None:
            return [initial_state] + path

    return None
