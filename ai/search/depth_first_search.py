from ai.search.exception import (
    NoValidPathException,
    InputException,
    DepthLimitReachedException,
)


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
    return _search(initial_state, goal_state, limit)


def _search(initial_state, goal_state, limit):
    if initial_state is None or goal_state is None:
        raise InputException("Initial state and goal state cannot be None.")

    if limit is not None:
        if limit <= 0:
            raise DepthLimitReachedException()
        limit -= 1

    if initial_state == goal_state:
        return [goal_state]

    depth_limit_reached = len(initial_state.edges) > 0
    for _, child_node in initial_state.edges:
        try:
            path = _search(child_node, goal_state, limit)
        except DepthLimitReachedException:
            pass
        except NoValidPathException:
            depth_limit_reached = False
        else:
            return [initial_state] + path

    if depth_limit_reached:
        raise DepthLimitReachedException()
    else:
        raise NoValidPathException()