from ai.search.classical.a_star import search
from ai.search.problem.graph import GraphProblem
from examples.util import convert_maze_to_nodes, maze_1


def manhattan_distance(start_node, end_node):
    return abs(start_node.row - end_node.row) + abs(start_node.col - end_node.col)


def main():
    nodes = convert_maze_to_nodes(maze_1)
    start = nodes[f"({len(maze_1)-1},{0})"]
    end = nodes[f"({0},{len(maze_1[0])-1})"]
    problem = GraphProblem(start, end)
    print(search(problem, manhattan_distance))


if __name__ == "__main__":
    main()
