import argparse
from collections import defaultdict
from copy import deepcopy

from ai.problem.wumpus_world import WumpusWorld

"""
Runs probabilistic logic to complete a path to the gold while avoiding pits
and the wumpus. Using Breeze and Stench flags in explored spaces, it infers the best
next move given likelihood of safety.
    `P(P(successor_node) | known, b) = 
        αP(successor_node) * SUM(P(b | known, P(successor_node), frontier)*P(frontier))`
    
    where `P(b | known, P(successor_node), frontier)` is 1 when P(successor_node) has
    a pit and 0 otherwise; α is a normalizing factor.
    
Default state operates on the default Wumpus World giving the below results:
    Initial Map
    | ['start']            | ['breeze', 'stench'] | ['wumpus']            |
    | ['breeze']           | ['pit']              | ['breeze', 'stench']  |
    | []                   | ['breeze']           | ['gold']              |
    
    Path Followed
    | X                    | X                    | ['wumpus']            |
    | X                    | ['pit']              | ['breeze', 'stench']  |
    | X                    | X                    | X                     |
"""

WUMPUS = "wumpus"
PIT = "pit"


def main(config):
    if config.random_world:
        problem = WumpusWorld.random_world()
    else:
        problem = WumpusWorld.default_world()
    current_state = problem.start_location

    explored = {current_state}
    frontier = {}

    path = [current_state]
    while not problem.is_terminal(current_state):
        for successor_tuple in problem.generate_successors(current_state):
            successor = (successor_tuple.row, successor_tuple.col)
            if successor not in explored:
                frontier[successor] = None

        worlds_a = generate_possible_permutations(problem, explored, frontier)
        worlds = strip_duplicates(worlds_a)
        if len(worlds) == 0:
            break
        probabilities = defaultdict(lambda: (0.0, 0.0))
        for node in frontier.keys():
            true_pit_probability, false_pit_probability = 0.0, 0.0
            true_wumpus_probability, false_wumpus_probability = 0.0, 0.0
            for world in worlds:
                if PIT in world[node]:
                    true_pit_probability += get_pit_probability(problem, world)
                else:
                    false_pit_probability += get_pit_probability(problem, world)

                if WUMPUS in world[node]:
                    true_wumpus_probability += get_wumpus_probability(problem, world)
                else:
                    false_wumpus_probability += get_wumpus_probability(problem, world)

            norm_true_pit_probability = true_pit_probability / (
                true_pit_probability + false_pit_probability
            )
            norm_false_pit_probability = false_pit_probability / (
                true_pit_probability + false_pit_probability
            )
            norm_true_wumpus_probability = true_wumpus_probability / (
                true_wumpus_probability + false_wumpus_probability
            )
            norm_false_wumpus_probability = false_wumpus_probability / (
                true_wumpus_probability + false_wumpus_probability
            )
            probabilities[node] = (
                norm_true_pit_probability * norm_true_wumpus_probability,
                norm_false_pit_probability * norm_false_wumpus_probability,
            )

        max_prob_safe = None
        max_successor = None
        for successor, prob in probabilities.items():
            _, false_prob = prob
            if max_successor is None or max_prob_safe < false_prob:
                max_prob_safe = false_prob
                max_successor = successor

        current_state = max_successor
        frontier.pop(current_state)
        path.append(current_state)
        explored.add(current_state)

    problem.visualize(path)
    return path


def get_pit_probability(problem, frontier):
    node_pit_probability = 1

    for other_node in frontier:
        if PIT in frontier[other_node]:
            node_pit_probability *= problem.pit_probability
        else:
            node_pit_probability *= 1 - problem.pit_probability

    return node_pit_probability


def get_wumpus_probability(problem, frontier):
    node_wumpus_probability = 1

    for other_node in frontier:
        if WUMPUS in frontier[other_node]:
            node_wumpus_probability *= problem.wumpus_probability
        else:
            node_wumpus_probability *= 1 - problem.wumpus_probability

    return node_wumpus_probability


def generate_possible_permutations(problem, explored, frontier):
    worlds = []
    for node, flags in frontier.items():
        if flags is not None:
            continue
        breeze = False
        stench = False
        for adjacent_tuple in problem.generate_successors(node):
            adjacent = (adjacent_tuple.row, adjacent_tuple.col)
            if adjacent in explored and problem.get_value(adjacent).breeze:
                breeze = True
            if adjacent in explored and problem.get_value(adjacent).stench:
                stench = True
            if breeze and stench:
                break

        new_frontier = deepcopy(frontier)
        new_frontier[node] = []
        worlds += generate_possible_permutations(problem, explored, new_frontier)
        if breeze:
            new_frontier[node] = {PIT: True}
            worlds += generate_possible_permutations(problem, explored, new_frontier)

        if stench:
            new_frontier[node] = {WUMPUS: True}
            worlds += generate_possible_permutations(problem, explored, new_frontier)

    if len(worlds) == 0:
        if verify_world(problem, explored, frontier):
            return [frontier]
        else:
            return []
    else:
        return worlds


def verify_world(problem, explored, frontier):
    for explored_node in explored:
        if problem.get_value(explored_node).breeze:
            valid = False
            for adjacent_tuple in problem.generate_successors(explored_node):
                adjacent = (adjacent_tuple.row, adjacent_tuple.col)
                if (
                    adjacent in frontier
                    and frontier[adjacent] is not None
                    and PIT in frontier[adjacent]
                ):
                    valid = True
            if not valid:
                return False

        if problem.get_value(explored_node).stench:
            valid = False
            for adjacent_tuple in problem.generate_successors(explored_node):
                adjacent = (adjacent_tuple.row, adjacent_tuple.col)
                if (
                    adjacent in frontier
                    and frontier[adjacent] is not None
                    and WUMPUS in frontier[adjacent]
                ):
                    valid = True
            if not valid:
                return False
    return True


def strip_duplicates(worlds):
    stripped_worlds = {}
    for world in worlds:
        stripped_worlds[str(world)] = world

    return list(stripped_worlds.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run probabilistic agent on wumpus world."
    )
    parser.add_argument(
        "--random_world", action="store_true", help="Generate a random world.",
    )
    main(parser.parse_args())
