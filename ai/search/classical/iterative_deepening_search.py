from ai.search.classical.depth_first_search import search as dfs
from ai.search.exception import DepthLimitReachedException


def search(problem):
    """

        Args:
            problem (GraphProblem)

        Returns:
            List[GraphNode] - optimal path from initial_state to goal_state
        """
    depth = 1
    while True:
        try:
            path = dfs(problem, depth)
        except DepthLimitReachedException:
            depth += 1
            pass
        else:
            return path
