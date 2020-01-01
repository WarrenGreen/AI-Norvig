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


def get_stochastic_successor(problem, current_state, stop_criteria_op):
    """ Get random uphill successor proportional to steepness. """
    uphill_successors = []
    current_value = problem.get_value(current_state)
    total_value = 0
    for successor in problem.generate_successors(current_state):
        successor_value = problem.get_value(successor)
        if stop_criteria_op(current_value, successor_value):
            total_value += successor_value
            uphill_successors.append((successor, successor_value))

    # Randomly choose a successor proportionally to their steepness
    successor_index = randint(0, total_value - 1)
    index = 0
    outer_index = 0
    mid_index = 0
    while index < successor_index:
        mid_index += 1
        index += 1
        if mid_index >= uphill_successors[outer_index][1]:
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


def search(problem, sideways_moves=False, successor_mode="steepest"):
    """

    Args:
        problem (Problem):
        sideways_moves (bool): Allow sideways moves on plateaus
        successor_mode (str): Which successor selection mode to choose.
                                ["steepest", "first-choice", "stochastic"]

    Returns:
        Tuple[List, int] solution state and solution value

    """
    current_state = problem.create_start()
    current_value = problem.get_value(current_state)
    if sideways_moves:
        stop_criteria_op = operator.lt
    else:
        stop_criteria_op = operator.le

    while True:
        if successor_mode == "first-choice":
            successor, successor_value = get_first_choice_successor(
                problem, current_state, stop_criteria_op
            )
        elif successor_mode == "stochastic":
            successor, successor_value = get_stochastic_successor(
                problem, current_state, stop_criteria_op
            )
        elif successor_mode == "steepest":
            successor, successor_value = get_best_successor(problem, current_state)
        else:
            raise ValueError(f"Invalid successor mode chosen. Must be one of: {SUCCESSOR_MODES}")

        if stop_criteria_op(successor_value, current_value):
            return current_state, current_value
        else:
            current_state = successor
            current_value = successor_value
