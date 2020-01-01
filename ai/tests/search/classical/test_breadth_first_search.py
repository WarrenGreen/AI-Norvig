import pytest

from ai.search.classical.exception import NoValidPathException, InputException
from ai.search.classical.node import GraphNode
from ai.search.classical.breadth_first_search import search


def test_search(unweighted_graph):
    root, goal = unweighted_graph
    path = search(root, goal)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_invalid_goal(unweighted_graph):
    root, goal = unweighted_graph
    with pytest.raises(NoValidPathException):
        path = search(root, GraphNode("invalid"))

    with pytest.raises(InputException):
        path = search(root, None)


def test_search_invalid_start(unweighted_graph):
    root, goal = unweighted_graph
    with pytest.raises(InputException):
        path = search(None, goal)
