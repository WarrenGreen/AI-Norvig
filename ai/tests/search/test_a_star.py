import pytest

from ai.search.exception import InputException, NoValidPathException
from ai.search.node import GraphNode
from ai.search.a_star import search


def test_search(graph):
    root, goal = graph
    path = search(root, goal, lambda x, y: 0)
    assert len(path) == 4
    assert path[0].name == "Sibiu"
    assert path[1].name == "Rimnicu Vilcea"
    assert path[2].name == "Pitesti"
    assert path[3].name == "Bucharest"


def test_search_invalid_goal(graph):
    root, goal = graph
    with pytest.raises(NoValidPathException):
        path = search(root, GraphNode("invalid"), lambda x, y: 0)

    with pytest.raises(InputException):
        path = search(root, None, lambda x, y: 0)


def test_search_invalid_start(graph):
    root, goal = graph
    with pytest.raises(InputException):
        path = search(None, goal, lambda x, y: 0)
