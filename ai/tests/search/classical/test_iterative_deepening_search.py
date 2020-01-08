import pytest

from ai.search.classical.iterative_deepening_search import search
from ai.search.exception import NoValidPathException
from ai.search.problem.node import GraphNode


def test_search(tree_problem):
    path = search(tree_problem)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_non_optimal(graph_problem):
    path = search(graph_problem)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_invalid_goal(tree_problem):
    tree_problem.goal_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(tree_problem)


def test_search_invalid_start(tree_problem):
    tree_problem.start_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(tree_problem)
