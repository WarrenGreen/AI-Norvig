import pytest

from ai.search.classical.a_star import search
from ai.search.exception import NoValidPathException
from ai.search.problem.node import GraphNode


def test_search(graph_problem):
    path = search(graph_problem, lambda x, y: 0)
    assert len(path) == 4
    assert path[0].name == "Sibiu"
    assert path[1].name == "Rimnicu Vilcea"
    assert path[2].name == "Pitesti"
    assert path[3].name == "Bucharest"


def test_search_invalid_goal(graph_problem):
    graph_problem.goal_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(graph_problem, lambda x, y: 0)


def test_search_invalid_start(graph_problem):
    graph_problem.start_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(graph_problem, lambda x, y: 0)
