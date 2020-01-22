import pytest

from ai.search.classical.iterative_deepening_a_star import search
from ai.search.exception import NoValidPathException
from ai.problem.node import GraphNode


def test_search(tree_problem):
    path = search(tree_problem, lambda x, y: 0)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_non_optimal(graph_problem):
    path = search(graph_problem, lambda x, y: 0)
    assert len(path) == 4
    assert path[0].name == "Sibiu"
    assert path[1].name == "Rimnicu Vilcea"
    assert path[2].name == "Pitesti"
    assert path[3].name == "Bucharest"


def test_search_invalid_goal(tree_problem):
    tree_problem.goal_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(tree_problem, lambda x, y: 0)


def test_search_invalid_start(tree_problem):
    tree_problem.start_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(tree_problem, lambda x, y: 0)
