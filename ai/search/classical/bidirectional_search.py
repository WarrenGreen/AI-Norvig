from ai.search.classical.breadth_first_search import BFS
from ai.search.classical.exception import NoValidPathException


def search(initial_state, goal_state):
    """

        Args:
            initial_state (GraphNode):
            goal_state (GraphNode):

        Returns:
            List[GraphNode] - optimal path from initial_state to goal_state
        """
    bfs_forward = BFS(initial_state, goal_state)
    bfs_backward = BFS(goal_state, initial_state)

    while not bfs_forward.is_finished and not bfs_backward.is_finished:
        bfs_forward.step()
        bfs_backward.step()
        if bfs_backward.current_node in bfs_forward.explored:
            backward_path = bfs_backward.explored[bfs_backward.current_node][:-1]
            path = bfs_forward.explored[bfs_backward.current_node] + list(
                reversed(backward_path)
            )
            return path

    raise NoValidPathException("No valid path between initial state and goal state.")
