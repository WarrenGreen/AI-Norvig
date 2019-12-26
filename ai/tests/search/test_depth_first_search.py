import pytest

from ai.src.search.node import GraphNode
from ai.src.search.depth_first_search import search


def test_search(tree):
    root, goal = tree
    path = search(root, goal)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_invalid_goal(tree):
    root, goal = tree
    with pytest.raises(ValueError):
        path = search(root, GraphNode("invalid", []))

    with pytest.raises(ValueError):
        path = search(root, None)


def test_search_invalid_start(tree):
    root, goal = tree
    with pytest.raises(ValueError):
        path = search(None, goal)