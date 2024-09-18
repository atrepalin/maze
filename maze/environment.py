import numpy as np
import matplotlib.pyplot as plt
from utils import plotlive

fig, ax = plt.subplots()


class State:
    def __init__(self, maze, position, goal):
        # Получаем размеры лабиринта
        y = len(maze)
        x = len(maze[0])

        # Устанавливаем границы лабиринта
        self.boundry = np.array([x, y])

        # Устанавливаем начальную и конечную точки
        self.position = position
        self.goal = goal
        self.maze = maze

    def check_boundaries(self, position):
        # Проверяем, выходит ли позиция за границы лабиринта
        out = len([num for num in position if num < 0])
        out += len([num for num in (self.boundry - np.asarray(position)) if num <= 0])
        return out > 0

    def check_walls(self, position):
        # Проверяем, является ли позиция стеной
        return self.maze[tuple(position)] == 1

    @property
    def valid(self):
        if self.check_boundaries(self.position):
            return False
        elif self.check_walls(self.position):
            return False
        return True

    @property
    def finished(self):
        return (self.position == self.goal).all()

    @plotlive
    def draw(self):
        plt.imshow(self.maze, interpolation="none", aspect="equal", cmap="Greys")

        plt.xticks([], [])
        plt.yticks([], [])

        ax.plot(self.goal[1], self.goal[0], "bs", markersize=4)  # Отметка цели
        ax.plot(
            self.position[1], self.position[0], "rs", markersize=4
        )  # Отметка стартовой позиции


action_map = {0: [0, 1], 1: [0, -1], 2: [1, 0], 3: [-1, 0]}


def make_move(state: State, action: int) -> State:
    current_position = state.position

    move = action_map[action]

    next_position = current_position + np.asarray(move)

    return State(state.maze, next_position, state.goal)
