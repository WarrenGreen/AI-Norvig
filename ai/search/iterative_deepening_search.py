from ai.search.depth_first_search import search as dfs
from ai.search.exception import DepthLimitReachedException


def search(initial_state, goal_state):
    """

        Args:
            initial_state ((Union[GraphNode, TreeNode])):
            goal_state ((Union[GraphNode, TreeNode])):

        Returns:
            List[(Union[GraphNode, TreeNode])] - optimal path from initial_state to goal_state
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
