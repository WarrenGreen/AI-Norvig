import pytest

from ai.search.classical.exception import InputException, NoValidPathException
from ai.search.classical.node import GraphNode
from ai.search.classical.uniform_cost_search import search


def test_search(graph):
    root, goal = graph
    path = search(root, goal)
    assert len(path) == 4
    assert path[0].name == "Sibiu"
    assert path[1].name == "Rimnicu Vilcea"
    assert path[2].name == "Pitesti"
    assert path[3].name == "Bucharest"


def test_search_invalid_goal(graph):
    root, goal = graph
    with pytest.raises(NoValidPathException):
        path = search(root, GraphNode("invalid"))

    with pytest.raises(InputException):
        path = search(root, None)


def test_search_invalid_start(graph):
    root, goal = graph
    with pytest.raises(InputException):
        path = search(None, goal)
