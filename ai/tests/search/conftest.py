import pytest

from ai.search.node import GraphNode


@pytest.fixture
def unweighted_graph():
    bucharest = GraphNode(name="Bucharest")
    sibiu = GraphNode(name="Sibiu")
    fagaras = GraphNode(name="Fagaras")
    rimnicu = GraphNode(name="Rimnicu Vilcea")
    pitesti = GraphNode(name="Pitesti")
    sibiu.add_edge(1, fagaras)
    sibiu.add_edge(1, rimnicu)
    fagaras.add_edge(1, bucharest)
    rimnicu.add_edge(1, pitesti)
    pitesti.add_edge(1, bucharest)

    return sibiu, bucharest


@pytest.fixture
def graph():
    bucharest = GraphNode(name="Bucharest")
    sibiu = GraphNode(name="Sibiu")
    fagaras = GraphNode(name="Fagaras")
    rimnicu = GraphNode(name="Rimnicu Vilcea")
    pitesti = GraphNode(name="Pitesti")
    sibiu.add_edge(99, fagaras)
    sibiu.add_edge(80, rimnicu)
    fagaras.add_edge(211, bucharest)
    rimnicu.add_edge(97, pitesti)
    pitesti.add_edge(101, bucharest)

    return sibiu, bucharest


@pytest.fixture
def tree():
    goal = GraphNode(name="Bucharest")
    root = GraphNode(name="Sibiu")
    root.edges.append((1, GraphNode(name="Fagaras")))
    root.edges.append((1, GraphNode(name="Rimnicu Vilcea")))
    root.edges[0][1].edges.append((1, goal))
    root.edges[1][1].edges.append((1, GraphNode(name="Pitesti")))

    return root, goal
