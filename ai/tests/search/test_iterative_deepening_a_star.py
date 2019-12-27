import pytest

from ai.search.exception import InputException, NoValidPathException
from ai.search.node import GraphNode
from ai.search.iterative_deepening_a_star import search


def test_search(tree):
    root, goal = tree
    path = search(root, goal, lambda x: 0)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_non_optimal(graph):
    root, goal = graph
    path = search(root, goal, lambda x: 0)
    assert len(path) == 4
    assert path[0].name == "Sibiu"
    assert path[1].name == "Rimnicu Vilcea"
    assert path[2].name == "Pitesti"
    assert path[3].name == "Bucharest"


def test_search_invalid_goal(tree):
    root, goal = tree
    with pytest.raises(NoValidPathException):
        path = search(root, GraphNode("invalid"), lambda x: 0)

    with pytest.raises(InputException):
        path = search(root, None, lambda x: 0)


def test_search_invalid_start(tree):
    root, goal = tree
    with pytest.raises(InputException):
        path = search(None, goal, lambda x: 0)
