# Автор: Трепалин А. А.
# Программа: Робот в лабиринте
# Описание: Данная программа реализует различные алгоритмы поиска пути для навигации робота по лабиринту.
# Робот может использовать такие алгоритмы, как метод ветвей и границ, поиск в глубину (с и без эвристики),
# поиск в ширину, двунаправленный поиск и алгоритм равных цен для нахождения оптимального пути.
# Версия: 08.10.2024

from functools import partial
import getopt
import sys
from time import sleep
from maze import load, State, make_move
import numpy as np

from solvers import bfs, dfs, dfs_with_cmp, ucs, bnb, bidirectional_search


def print_header():
    print("##############################################")
    print("# Author: Trepalin A. A.")
    print("# Program: Robot in a Maze")
    print(
        "# Description: This program implements various search algorithms to navigate a robot through a maze. "
    )
    print(
        "# The robot can use algorithms such as Branch and Bound, Depth-First Search (with and without heuristic), "
    )
    print("# Breadth-first search, Bidirectional search and Uniform Cost Search to find the optimal path.")
    print("# Version: 08.10.2024")
    print("##############################################")


def main(argv):
    print_header()

    opts = dict(getopt.getopt(argv, "f:s:")[0])

    if "-f" in opts:
        file = opts["-f"]
    else:
        file = input("Enter maze file name: ")

    if not file.endswith(".npy"):
        print("Invalid file. Exiting...")
        exit()

    print("Loading maze from " + file)
    maze = load(file)

    state = State(maze, np.array([0, 0]), maze.shape - np.asarray([1, 1]))

    goal_state = State(
        maze, maze.shape - np.asarray([1, 1]), maze.shape - np.asarray([1, 1])
    )

    solvers = {
        "bfs": bfs,
        "dfs": dfs,
        "dfs_with_cmp": dfs_with_cmp,
        "ucs": ucs,
        "bnb": bnb,
        "bidirectional_search": partial(bidirectional_search, goal_state=goal_state),
    }

    if "-s" in opts:
        solver = opts["-s"]
    else:
        solver = input(
            "Enter solver (bfs, dfs, dfs_with_cmp, ucs, bnb, bidirectional_search): "
        )

    if solver not in solvers:
        print("Invalid solver. Exiting...")
        exit()

    print("Solver: " + solver)

    actions = solvers[solver](state)

    if actions is None:
        print("No solution found. Exiting...")
        exit()

    for action in actions:
        state = make_move(state, action)
        state.draw()
        sleep(0.1)

    input()


if __name__ == "__main__":
    main(sys.argv[1:])
