import pytest

from ai.search.classical.exception import (
    InputException,
    NoValidPathException,
    DepthLimitReachedException,
)
from ai.search.classical.node import GraphNode
from ai.search.classical.depth_first_search import search


def test_search(tree):
    root, goal = tree
    path = search(root, goal)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_depth_limited(tree):
    root, goal = tree
    with pytest.raises(DepthLimitReachedException):
        path = search(root, goal, 1)

    with pytest.raises(DepthLimitReachedException):
        path = search(root, goal, 2)

    path = search(root, goal, 3)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"

    path = search(root, goal, 10)
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
