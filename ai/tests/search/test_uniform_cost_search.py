import pytest

from ai.src.search.node import GraphNode
from ai.src.search.uniform_cost_search import search


@pytest.fixture
def tree():
    goal = GraphNode(name="Bucharest", edges=[])
    root = GraphNode(name="Sibiu", edges=[])
    root.edges.append((99, GraphNode(name="Fagaras", edges=[])))
    root.edges.append((80, GraphNode(name="Rimnicu Vilcea", edges=[])))
    root.edges[0][1].edges.append((211, goal))
    root.edges[1][1].edges.append(
        (97, GraphNode(name="Pitesti", edges=[]))
    )
    root.edges[1][1].edges[0][1].edges.append((101, goal))

    return root, goal


def test_search(tree):
    root, goal = tree
    path = search(root, goal)
    assert len(path) == 4
    assert path[0].name == "Sibiu"
    assert path[1].name == "Rimnicu Vilcea"
    assert path[2].name == "Pitesti"
    assert path[3].name == "Bucharest"


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
