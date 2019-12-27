from typing import NamedTuple, List, Tuple

from ai.search.exception import InputException


class GraphNode:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, cost, node):
        self.edges.append((cost, node))
        for _, n in node.edges:
            if self == n:
                raise InputException(
                    f"{str(self)} already exists in edge list for {str(node)}"
                )
        node.edges.append((cost, self))

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"GraphNode<{self.name}>"
