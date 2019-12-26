import pytest

from ai.src.search.node import GraphNode
from ai.src.search.breadth_first_search import search


def test_search(unweighted_graph):
    root, goal = unweighted_graph
    path = search(root, goal)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_invalid_goal(unweighted_graph):
    root, goal = unweighted_graph
    with pytest.raises(ValueError):
        path = search(root, GraphNode("invalid", []))

    with pytest.raises(ValueError):
        path = search(root, None)


def test_search_invalid_start(unweighted_graph):
    root, goal = unweighted_graph
    with pytest.raises(ValueError):
        path = search(None, goal)
