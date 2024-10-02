from time import sleep
from maze import load, State, make_move
import numpy as np

from solvers import bfs, dfs, dfs_with_cmp, distance

maze = load("20x20.npy")

state = State(maze, np.array([0, 0]), np.array([19, 19]))

actions = dfs_with_cmp(state, distance)

for action in actions:
    state = make_move(state, action)
    state.draw()
    sleep(0.1)

input()
