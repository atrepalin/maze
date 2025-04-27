from functools import partial
import getopt
import sys
from analyzer.statistic import Statistic
from maze import load, Situation
import numpy as np

from solvers import bfs, dfs, dfs_with_cmp, ucs, bnb, bidirectional_search

from sys import setrecursionlimit

setrecursionlimit(10000)

def main(argv):
    try:
        opts = dict(getopt.getopt(argv, "f:")[0])
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

    solvers = [
        bfs,
        dfs,
        dfs_with_cmp,
        ucs,
        bnb,
        partial(bidirectional_search, goal_situation),
    ]

    solver_names = [
        "Breadth-first search",
        "Depth-first search",
        "DFS with comparison",
        "Uniform Cost Search",
        "Branch and Bound",
        "Bidirectional search",
    ]

    statistics = []

    for solver in solvers:
        _, statistic = solver(situation)
        statistics.append(statistic)

    Statistic.print_statistics(statistics, solver_names)


if __name__ == "__main__":
    main(sys.argv[1:])
