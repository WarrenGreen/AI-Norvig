import pytest

from ai.search.classical.breadth_first_search import search
from ai.search.exception import NoValidPathException
from ai.problem.node import GraphNode


def test_search(unweighted_graph_problem):
    path = search(unweighted_graph_problem)
    assert len(path) == 3
    assert path[0].name == "Sibiu"
    assert path[1].name == "Fagaras"
    assert path[2].name == "Bucharest"


def test_search_invalid_goal(unweighted_graph_problem):
    unweighted_graph_problem.goal_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(unweighted_graph_problem)


def test_search_invalid_start(unweighted_graph_problem):
    unweighted_graph_problem.start_node = GraphNode("invalid")
    with pytest.raises(NoValidPathException):
        path = search(unweighted_graph_problem)
