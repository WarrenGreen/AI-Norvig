import operator
from random import choice, randint

SUCCESSOR_MODES = ["steepest", "first-choice", "stochastic"]


def get_best_successor(problem, current_state):
    """ Get steepest successor"""
    best_successor = None
    best_successor_value = None
    for successor in problem.generate_successors(current_state):
        successor_value = problem.get_value(successor)
        if best_successor is None or successor_value > best_successor_value:
            best_successor = successor
            best_successor_value = successor_value

    return best_successor, best_successor_value


def get_stochastic_successor(problem, current_state, sideways_moves):
    """ Get random uphill successor proportional to steepness. """
    if sideways_moves:
        stop_criteria_op = operator.le
    else:
        stop_criteria_op = operator.lt
    uphill_successors = []
    current_value = problem.get_value(current_state)
    total_value = 0
    for successor in problem.generate_successors(current_state):
        successor_value = problem.get_value(successor)
        if stop_criteria_op(current_value, successor_value):
            total_value += successor_value
            uphill_successors.append((successor, successor_value))

    if total_value == 0:
        return None, None

    # Randomly choose a successor proportionally to their steepness
    successor_index = randint(0, abs(total_value) - 1)
    index = 0
    outer_index = 0
    mid_index = 0
    while index < successor_index:
        mid_index += 1
        index += 1
        if mid_index >= abs(uphill_successors[outer_index][1]):
            outer_index += 1
            mid_index = 0

    return uphill_successors[outer_index]


def get_first_choice_successor(problem, current_state, stop_criteria_op):
    """ Get first random generated uphill successor. """
    current_value = problem.get_value(current_state)
    for successor in problem.generate_successors(current_state):
        successor_value = problem.get_value(successor)
        if stop_criteria_op(current_value, successor_value):
            return successor, successor_value

    return None, 0


def search(
    problem, sideways_moves=False, successor_mode="steepest", max_sideways_moves=20
):
    """

    Args:
        problem (Problem):
        sideways_moves (bool): Allow sideways moves on plateaus
        successor_mode (str): Which successor selection mode to choose.
                                ["steepest", "first-choice", "stochastic"]
        max_sideways_moves(int): Maximum sideways moves to make in seqence before
            quitting to defend against a global maxima on a plateau

    Returns:
        Tuple[List, int] solution state and solution value

    """
    current_state = problem.create_start()
    current_value = problem.get_value(current_state)
    if sideways_moves:
        stop_criteria_op = operator.lt
    else:
        stop_criteria_op = operator.le

    sideways_count = 0
    while True:
        if successor_mode == "first-choice":
            successor, successor_value = get_first_choice_successor(
                problem, current_state, stop_criteria_op
            )
        elif successor_mode == "stochastic":
            successor, successor_value = get_stochastic_successor(
                problem, current_state, sideways_moves
            )
        elif successor_mode == "steepest":
            successor, successor_value = get_best_successor(problem, current_state)
        else:
            raise ValueError(
                f"Invalid successor mode chosen. Must be one of: {SUCCESSOR_MODES}"
            )

        if successor_value == current_value:
            sideways_count += 1

        if (
            successor is None
            or (max_sideways_moves is not None and sideways_count > max_sideways_moves)
            or stop_criteria_op(successor_value, current_value)
        ):
            return current_state, current_value
        else:
            current_state = successor
            current_value = successor_value
