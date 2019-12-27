from ai.search.depth_first_search import search as dfs
from ai.search.exception import DepthLimitReachedException


def search(initial_state, goal_state):
    """

        Args:
            initial_state (GraphNode):
            goal_state (GraphNode):

        Returns:
            List[GraphNode] - optimal path from initial_state to goal_state
        """
    depth = 1
    while True:
        try:
            path = dfs(initial_state, goal_state, depth)
        except DepthLimitReachedException:
            depth += 1
            pass
        else:
            return path
