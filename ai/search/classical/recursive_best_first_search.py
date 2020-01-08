from ai.search.exception import (
    NoValidPathException,
    CostLimitReachedException,
)


# TODO: Doesn't work yet
def search(problem, heuristic_fn):
    """

    Args:
        problem (GraphProblem):
        heuristic_fn (Callable[GraphNode, GraphNode]): function to estimate cost between parameter
                node and goal state

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    problem.start_node.f = 0 + heuristic_fn(problem.start_node, problem.goal_node)
    problem.start_node.g = 0
    _search(problem.start_node, problem.goal_node, [], 9999, heuristic_fn)


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
