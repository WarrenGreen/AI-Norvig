from ai.search.exception import (
    NoValidPathException,
    CostLimitReachedException,
    InputException,
)


# TODO: Doesn't work yet
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
    initial_state.f = 0 + heuristic_fn(initial_state, goal_state)
    initial_state.g = 0
    _search(initial_state, goal_state, [], 9999, heuristic_fn)


def _search(initial_state, goal_state, path, f_limit, heuristic_fn):
    if initial_state == goal_state:
        return path

    if len(initial_state.edges) == 0:
        raise NoValidPathException()

    for edge_cost, child_node in initial_state.edges:
        child_node.g = initial_state.g + edge_cost
        child_node.f = max(
            child_node.g + heuristic_fn(child_node, goal_state), initial_state.f
        )

    while True:
        best_node = None
        for _, child_node in initial_state.edges:
            if best_node is None or best_node.f > child_node.f:
                best_node = child_node

        if best_node.f > f_limit:
            raise CostLimitReachedException(best_node.f)

        alternative_node = None
        for _, child_node in initial_state.edges:
            if (
                alternative_node is None or alternative_node.f > child_node.f
            ) and alternative_node != best_node:
                alternative_node = child_node

        try:
            path = _search(
                initial_state=best_node,
                goal_state=goal_state,
                path=path + [best_node],
                f_limit=min(f_limit, alternative_node.f),
                heuristic_fn=heuristic_fn,
            )
        except CostLimitReachedException as ex:
            best_node.f = ex.cost
        else:
            return path
