import pytest

from ai.problem import GraphProblem
from ai.problem.node import GraphNode, TreeNode


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
    goal = TreeNode(name="Bucharest")
    root = TreeNode(name="Sibiu")
    root.add_edge(1, TreeNode(name="Fagaras"))
    root.add_edge(1, TreeNode(name="Rimnicu Vilcea"))
    root.edges[0][1].add_edge(1, goal)
    root.edges[1][1].add_edge(1, TreeNode(name="Pitesti"))

    return root, goal


@pytest.fixture
def graph_problem(graph):
    start_node, end_node = graph
    return GraphProblem(start_node, end_node)


@pytest.fixture
def unweighted_graph_problem(unweighted_graph):
    start_node, end_node = unweighted_graph
    return GraphProblem(start_node, end_node)


@pytest.fixture
def tree_problem(tree):
    start_node, end_node = tree
    return GraphProblem(start_node, end_node)
