from typing import NamedTuple, List, Tuple


class GraphNode(NamedTuple):
    name: str
    edges: List[Tuple[int, "GraphNode"]]
