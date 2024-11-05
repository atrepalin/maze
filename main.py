# Автор: Трепалин А. А.
# Программа: Робот в лабиринте
# Описание: Данная программа реализует различные алгоритмы поиска пути для навигации робота по лабиринту.
# Робот может использовать такие алгоритмы, как метод ветвей и границ, поиск в глубину (с и без эвристики),
# поиск в ширину, двунаправленный поиск и алгоритм равных цен для нахождения оптимального пути.
# Версия: 05.11.2024

from functools import partial
import getopt
import sys
from time import sleep
import keyboard
from maze import load, Situation, make_move
import numpy as np

from solvers import bfs, dfs, dfs_with_cmp, ucs, bnb, bidirectional_search
from utils import select_option


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
    print(
        "# Breadth-first search, Bidirectional search and Uniform Cost Search to find the optimal path."
    )
    print("# Version: 05.11.2024")
    print("##############################################")


def main(argv):
    print_header()

    try:
        opts = dict(getopt.getopt(argv, "f:s:")[0])
    except getopt.GetoptError:
        print("Invalid arguments. Exiting...")
        exit()

    if "-f" in opts:
        file = opts["-f"]
    else:
        file = input("Enter maze file name: ")

    if not file.endswith(".npy"):
        print("Invalid file. Exiting...")
        exit()

    print("Loading maze from " + file)
    maze = load(file)

    situation = Situation(maze, np.array([0, 0]), maze.shape - np.asarray([1, 1]))

    goal_situation = Situation(
        maze, maze.shape - np.asarray([1, 1]), maze.shape - np.asarray([1, 1])
    )

    solvers = {
        "bfs": bfs,
        "dfs": dfs,
        "dfs_with_cmp": dfs_with_cmp,
        "ucs": ucs,
        "bnb": bnb,
        "bidirectional_search": partial(bidirectional_search, goal_situation),
    }

    solver_options = list(solvers.keys())
    solver_names = [
        "Breadth-first search",
        "Depth-first search",
        "DFS with comparison",
        "Uniform Cost Search",
        "Branch and Bound",
        "Bidirectional search",
    ]

    if "-s" in opts:
        solver = opts["-s"]
    else:
        option = select_option(solver_names)
        solver = solver_options[option]

    if solver not in solvers:
        print("Invalid solver. Exiting...")
        exit()

    print("Solver: " + solver)

    actions, statistic = solvers[solver](situation)

    print(statistic)

    if actions is None:
        print("No solution found. Exiting...")
        exit()

    for action in actions:
        situation = make_move(situation, action)
        situation.draw()
        sleep(0.1)

    keyboard.read_event()


if __name__ == "__main__":
    main(sys.argv[1:])
