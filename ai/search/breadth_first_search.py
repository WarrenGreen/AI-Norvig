from ai.search.exception import InputException, NoValidPathException


class BFS:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.queue_1 = [(self.initial_state, [])]
        self.queue_2 = []
        self.explored = {}
        self.finished_path = None
        self.current_node = None

        if self.initial_state is None or self.goal_state is None:
            raise InputException("Initial state and goal state cannot be None.")

    def search(self):
        while len(self.queue_1) > 0:
            self.step()

    @property
    def is_finished(self):
        return len(self.queue_1) == 0 or self.finished_path is not None

    def step(self):
        node, path = self.queue_1.pop(0)
        self.current_node = node
        new_path = path + [node]
        self.explored[node] = new_path
        if node == self.goal_state:
            self.finished_path = new_path

        for edge_cost, child_node in node.edges:
            self.queue_2.append((child_node, new_path))

        if len(self.queue_1) == 0:
            self.queue_1 = self.queue_2
            self.queue_2 = []


def search(initial_state, goal_state):
    """

    Args:
        initial_state (GraphNode):
        goal_state (GraphNode):

    Returns:
        List[GraphNode] - optimal path from initial_state to goal_state
    """
    if initial_state is None or goal_state is None:
        raise InputException("Initial state and goal state cannot be None.")

    explored = set()
    queue_1 = [(initial_state, [])]
    queue_2 = []

    while len(queue_1) > 0:
        node, path = queue_1.pop(0)
        explored.add(node)
        new_path = path + [node]
        if node == goal_state:
            return new_path

        for edge_cost, child_node in node.edges:
            if child_node not in explored:
                queue_2.append((child_node, new_path))

        if len(queue_1) == 0:
            queue_1 = queue_2
            queue_2 = []

    raise NoValidPathException("No valid path between initial state and goal state.")
