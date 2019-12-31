from ai.search.classical.exception import (
    NoValidPathException,
    InputException,
    DepthLimitReachedException,
    CostLimitReachedException,
)


def search(
    initial_state,
    goal_state,
    depth_limit=None,
    cost_limit=None,
    *,
    heuristic_fn=lambda start, end: 0
):
    """
        Low-memory depth-first implementation.

        Args:
            initial_state (GraphNode):
            goal_state (GraphNode):
            depth_limit (Optional[int]): Maximum depth to traverse. `None` value
                signifies infinite depth.
            cost_limit (Optional[int]): Maximum cost to traverse. `None` value
                signifies infinite cost.
            heuristic_fn (Callable[GraphNode, GraphNode]): function to estimate cost
                between parameter node and goal state

        Returns:
            List[GraphNode] - optimal path from initial_state to goal_state
        """
    return _search(
        initial_state=initial_state,
        cost=0,
        goal_state=goal_state,
        depth_limit=depth_limit,
        cost_limit=cost_limit,
        explored=set(),
        heuristic_fn=heuristic_fn,
    )


def _search(
    initial_state, cost, goal_state, depth_limit, cost_limit, explored, heuristic_fn
):
    if initial_state is None or goal_state is None:
        raise InputException("Initial state and goal state cannot be None.")

    if depth_limit is not None:
        if depth_limit <= 0:
            raise DepthLimitReachedException()
        depth_limit -= 1

    if cost_limit is not None:
        if cost > cost_limit:
            raise CostLimitReachedException(cost)

    if initial_state == goal_state:
        return [goal_state]

    explored.add(initial_state)
    depth_limit_reached = 0
    cost_limit_reached = 0
    min_exceeding_cost = None
    for edge_cost, child_node in initial_state.edges:
        if child_node in explored:
            depth_limit_reached += 1
            cost_limit_reached += 1
            continue
        try:
            path = _search(
                initial_state=child_node,
                cost=cost + edge_cost + heuristic_fn(child_node, goal_state),
                goal_state=goal_state,
                depth_limit=depth_limit,
                cost_limit=cost_limit,
                explored=explored,
                heuristic_fn=heuristic_fn,
            )
        except DepthLimitReachedException:
            depth_limit_reached += 1
        except CostLimitReachedException as ex:
            cost_limit_reached += 1
            if min_exceeding_cost is None:
                min_exceeding_cost = ex.cost
            else:
                min_exceeding_cost = min(ex.cost, min_exceeding_cost)
        except NoValidPathException:
            pass
        else:
            return [initial_state] + path

    if 0 < len(initial_state.edges) == depth_limit_reached:
        raise DepthLimitReachedException()
    elif 0 < len(initial_state.edges) == cost_limit_reached:
        raise CostLimitReachedException(min_exceeding_cost)
    else:
        raise NoValidPathException()
