import pytest

from ai.search.node import GraphNode


@pytest.fixture
def unweighted_graph():
    goal = GraphNode(name="Bucharest", edges=[])
    root = GraphNode(name="Sibiu", edges=[])
    root.edges.append((1, GraphNode(name="Fagaras", edges=[])))
    root.edges.append((1, GraphNode(name="Rimnicu Vilcea", edges=[])))
    root.edges[0][1].edges.append((1, goal))
    root.edges[1][1].edges.append((1, GraphNode(name="Pitesti", edges=[])))
    root.edges[1][1].edges[0][1].edges.append((1, goal))

    return root, goal


@pytest.fixture
def graph():
    goal = GraphNode(name="Bucharest", edges=[])
    root = GraphNode(name="Sibiu", edges=[])
    root.edges.append((99, GraphNode(name="Fagaras", edges=[])))
    root.edges.append((80, GraphNode(name="Rimnicu Vilcea", edges=[])))
    root.edges[0][1].edges.append((211, goal))
    root.edges[1][1].edges.append((97, GraphNode(name="Pitesti", edges=[])))
    root.edges[1][1].edges[0][1].edges.append((101, goal))

    return root, goal


@pytest.fixture
def tree():
    goal = GraphNode(name="Bucharest", edges=[])
    root = GraphNode(name="Sibiu", edges=[])
    root.edges.append((1, GraphNode(name="Fagaras", edges=[])))
    root.edges.append((1, GraphNode(name="Rimnicu Vilcea", edges=[])))
    root.edges[0][1].edges.append((1, goal))
    root.edges[1][1].edges.append((1, GraphNode(name="Pitesti", edges=[])))

    return root, goal
