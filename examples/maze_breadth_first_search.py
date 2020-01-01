from ai.search.classical.breadth_first_search import search
from examples.util import convert_maze_to_nodes, maze_1


def main():
    nodes = convert_maze_to_nodes(maze_1)
    start = nodes[f"({len(maze_1)-1},{0})"]
    end = nodes[f"({0},{len(maze_1[0])-1})"]

    print(search(start, end))


if __name__ == "__main__":
    main()
