# Автор: Трепалин А. А.
# Программа: Робот в лабиринте
# Описание: Данная программа реализует различные алгоритмы поиска пути для навигации робота по лабиринту.
# Робот может использовать такие алгоритмы, как метод ветвей и границ, поиск в глубину (с и без эвристики),
# поиск в ширину и алгоритм равных цен для нахождения оптимального пути.
# Версия: 04.10.2024

from time import sleep
from maze import load, State
import numpy as np

from solvers import bfs, dfs, dfs_with_cmp, ucs, bnb


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
    print("# Breadth-first search, and Uniform Cost Search to find the optimal path.")
    print("# Version: 04.10.2024")
    print("##############################################")


print_header()

file = input("Enter maze file name: ")

maze = load(file)

state = State(maze, np.array([0, 0]), maze.shape - np.asarray([1, 1]))

solvers = {"bfs": bfs, "dfs": dfs, "dfs_with_cmp": dfs_with_cmp, "ucs": ucs, "bnb": bnb}

solver = input("Enter solver (bfs, dfs, dfs_with_cmp, ucs, bnb): ")

if solver not in solvers:
    print("Invalid solver. Exiting...")
    exit()

actions = solvers[solver](state)

if actions is None:
    print("No solution found. Exiting...")
    exit()

for action in actions:
    state = state.make_move(action)
    state.draw()
    sleep(0.1)

input()
