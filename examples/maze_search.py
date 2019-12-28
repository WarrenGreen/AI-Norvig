from ai.search.breadth_first_search import search
from ai.search.exception import InputException
from ai.search.node import GraphNode

maze_1 = [
    ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "X", "O", "O", "O", "O", "O", "X", "X", "X", "O", "O"],
    ["O", "O", "O", "X", "X", "O", "O", "O", "O", "O", "X", "O", "X", "O", "O"],
    ["O", "O", "X", "O", "X", "O", "O", "O", "O", "O", "X", "O", "X", "O", "O"],
    ["O", "X", "O", "O", "O", "X", "O", "O", "O", "O", "X", "X", "X", "O", "O"],
    ["O", "X", "O", "O", "O", "X", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "X", "O", "O", "O", "O", "X", "O", "O", "X", "X", "O", "O", "O", "O"],
    ["O", "X", "X", "X", "X", "X", "X", "O", "O", "X", "O", "X", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O", "O", "X", "O", "X", "O", "X", "X"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "O", "X", "O", "X", "O", "X", "X"],
    ["O", "X", "O", "O", "O", "O", "O", "X", "O", "X", "X", "O", "O", "X", "X"],
    ["O", "X", "O", "O", "O", "O", "O", "X", "O", "X", "O", "O", "X", "O", "X"],
    ["O", "X", "O", "O", "O", "O", "O", "X", "O", "O", "O", "X", "O", "O", "X"],
    ["O", "X", "O", "O", "O", "O", "O", "X", "O", "O", "X", "O", "O", "O", "X"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X"],
    ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
]


def convert_maze_to_nodes(maze):
    nodes = {}
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "X":
                continue
            node = GraphNode(f"({i},{j})")
            nodes[f"({i},{j})"] = node
            for ii, jj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                if i + ii < 0 or i + ii >= len(maze) or j + jj < 0 or j + jj >= len(
                        maze[0]):
                    continue

                key = f"({i + ii},{j + jj})"
                if key in nodes:
                    try:
                        node.add_edge(1, nodes[key])
                    except InputException:
                        pass
    return nodes


def main():
    nodes = convert_maze_to_nodes(maze_1)
    start = nodes[f"({len(maze_1)-1},{0})"]
    end = nodes[f"({0},{len(maze_1[0])-1})"]

    print(search(start, end))


if __name__ == '__main__':
    main()
