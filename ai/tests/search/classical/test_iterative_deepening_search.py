import pytest

from ai.search.classical.exception import InputException, NoValidPathException
from ai.search.classical.node import GraphNode
from ai.search.classical.iterative_deepening_search import search


def test_search(tree):
    root, goal = tree
    path = search(root, goal)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_non_optimal(graph):
    root, goal = graph
    path = search(root, goal)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_invalid_goal(tree):
    root, goal = tree
    with pytest.raises(NoValidPathException):
        path = search(root, GraphNode("invalid"))

    with pytest.raises(InputException):
        path = search(root, None)


def test_search_invalid_start(tree):
    root, goal = tree
    with pytest.raises(InputException):
        path = search(None, goal)
