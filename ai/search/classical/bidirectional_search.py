from ai.search.classical.breadth_first_search import BFS
from ai.search.exception import NoValidPathException
from ai.search.problem.graphproblem import GraphProblem


def search(problem):
    """

        Args:
            problem(GraphProblem): 

        Returns:
            List[GraphNode] - optimal path from initial_state to goal_state
        """
    bfs_forward = BFS(problem)
    problem_backward = GraphProblem(
        start_node=problem.goal_node, goal_node=problem.start_node
    )
    bfs_backward = BFS(problem_backward)

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
