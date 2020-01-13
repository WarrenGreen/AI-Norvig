from collections import defaultdict
from copy import deepcopy

from ai.search.problem.wumpus_world import WumpusWorld

"""
Runs probabilistic logic to complete a path to the gold while avoiding pits
and the wumpus. Using Breeze and Stench flags in explored spaces, it infers the best
next move given likelihood of safety.
    `P(P(successor_node) | known, b) = 
        αP(successor_node) * SUM(P(b | known, P(successor_node), frontier)*P(frontier))`
    
    where `P(b | known, P(successor_node), frontier)` is 1 when P(successor_node) has
    a pit and 0 otherwise.
"""


def main():
    problem = WumpusWorld.default_world()
    current_state = "0,0"

    explored = {current_state}
    frontier = {}

    path = [current_state]
    while not problem.is_terminal(current_state):
        for successor in problem.generate_successors(current_state):
            if successor not in explored:
                frontier[successor] = None

        worlds = generate_possible_permutations(problem, explored, frontier)
        worlds = strip_duplicates(worlds)
        probabilities = defaultdict(lambda: (0, 0))
        for node in frontier.keys():
            true_pit_probability, false_pit_probability = 0.0, 0.0
            true_wumpus_probability, false_wumpus_probability = 0.0, 0.0
            for world in worlds:
                if WumpusWorld.PIT in world[node]:
                    true_pit_probability += get_pit_probability(problem, world)
                else:
                    false_pit_probability += get_pit_probability(problem, world)

                if WumpusWorld.WUMPUS in world[node]:
                    true_wumpus_probability += get_wumpus_probability(problem, world)
                else:
                    false_wumpus_probability += get_wumpus_probability(problem, world)

            norm_true_pit_probability = true_pit_probability / (true_pit_probability + false_pit_probability)
            norm_false_pit_probability = false_pit_probability / (true_pit_probability + false_pit_probability)
            norm_true_wumpus_probability = true_wumpus_probability / (
                        true_wumpus_probability + false_wumpus_probability)
            norm_false_wumpus_probability = false_wumpus_probability / (
                        true_wumpus_probability + false_wumpus_probability)
            probabilities[node] = (norm_true_pit_probability*norm_true_wumpus_probability, norm_false_pit_probability*norm_false_wumpus_probability)

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
        if WumpusWorld.PIT in frontier[other_node]:
            node_pit_probability *= problem.pit_probability
        else:
            node_pit_probability *= 1 - problem.pit_probability

    return node_pit_probability


def get_wumpus_probability(problem, frontier):
    node_wumpus_probability = 1

    for other_node in frontier:
        if WumpusWorld.WUMPUS in frontier[other_node]:
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
        for adjacent in problem.generate_successors(node):
            if adjacent in explored and WumpusWorld.BREEZE in problem.get_value(adjacent):
                breeze = True
            if adjacent in explored and WumpusWorld.STENCH in problem.get_value(adjacent):
                stench = True
            if breeze and stench:
                break

        new_frontier = deepcopy(frontier)
        new_frontier[node] = []
        worlds += generate_possible_permutations(problem, explored, new_frontier)
        if breeze:
            new_frontier[node] = [WumpusWorld.PIT]
            worlds += generate_possible_permutations(problem, explored, new_frontier)

        if stench:
            new_frontier[node] = [WumpusWorld.WUMPUS]
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
        if WumpusWorld.BREEZE in problem.get_value(explored_node):
            valid = False
            for adjacent in problem.generate_successors(explored_node):
                if adjacent in frontier and frontier[adjacent] is not None and WumpusWorld.PIT in frontier[adjacent]:
                    valid = True
            if not valid:
                return False

        if WumpusWorld.STENCH in problem.get_value(explored_node):
            valid = False
            for adjacent in problem.generate_successors(explored_node):
                if adjacent in frontier and frontier[adjacent] is not None and WumpusWorld.WUMPUS in frontier[adjacent]:
                    valid = True
            if not valid:
                return False
    return True


def strip_duplicates(worlds):
    stripped_worlds = {}
    for world in worlds:
        stripped_worlds[str(world)] = world

    return list(stripped_worlds.values())


if __name__ == '__main__':
    main()
