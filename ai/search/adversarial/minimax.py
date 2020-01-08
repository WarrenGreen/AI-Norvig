def search(problem, state=None, max_depth=None):
    """
    Generic Min-Max Tree Solver
    Args:
        problem (Problem):
        state (List[str])):
        max_depth (int): Maximum ply depth to search. `None` infers infinity.

    Returns:
        (Tuple[List[str], int]) - best next move and the value associated with it
    """
    if state is None:
        state = problem.create_start()

    return max_value(problem, state, max_depth)


def max_value(problem, state, max_depth):
    if max_depth is not None:
        if max_depth <= 0:
            return state, problem.get_value(state)
        else:
            max_depth -= 1

    if problem.is_terminal(state):
        return state, problem.get_value(state)

    max_val = None
    max_state = None
    for successor in problem.generate_successors(state):
        successor_state, successor_value = min_value(problem, successor, max_depth)
        if max_val is None or successor_value > max_val:
            max_val = successor_value
            max_state = successor

    return max_state, max_val


def min_value(problem, state, max_depth):
    if max_depth is not None:
        if max_depth <= 0:
            return state, problem.get_value(state)
        else:
            max_depth -= 1

    if problem.is_terminal(state):
        return state, problem.get_value(state)

    min_val = None
    min_state = None
    for successor in problem.generate_successors(state):
        successor_state, successor_value = max_value(problem, successor, max_depth)
        if min_val is None or successor_value < min_val:
            min_val = successor_value
            min_state = successor

    return min_state, min_val
