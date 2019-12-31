from ai.search.depth_first_search import search as dfs
from ai.search.exception import CostLimitReachedException


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
    cost_limit = 1
    while True:
        try:
            path = dfs(
                initial_state=initial_state,
                goal_state=goal_state,
                cost_limit=cost_limit,
                heuristic_fn=heuristic_fn,
            )
        except CostLimitReachedException as ex:
            cost_limit = ex.cost
        else:
            return path
