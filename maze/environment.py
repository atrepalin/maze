import numpy as np
import matplotlib.pyplot as plt
from utils import plotlive

fig, ax = plt.subplots()


class Situation:
    def __init__(self, maze, position, goal):
        """
        Создаёт экземпляр класса Situation, хранящий информацию о состоянии лабиринта.

        :param maze: матрица, представляющая лабиринт
        :type maze: numpy 2D array
        :param position: координаты стартовой позиции
        :type position: numpy 1D array
        :param goal: координаты целевой позиции
        :type goal: numpy 1D array
        """

        # Устанавливаем границы лабиринта
        self.boundry = maze.shape

        # Устанавливаем начальную и конечную точки
        self.position = position
        self.goal = goal
        self.maze = maze

    def check_boundaries(self, position):
        """Проверяет, находится ли position за пределами лабиринта.

        :param position: координаты, которые необходимо проверить
        :type position: numpy 1D array
        :return: True, если position за пределами, False - иначе
        :rtype: bool
        """

        out = len([num for num in position if num < 0])
        out += len([num for num in (self.boundry - np.asarray(position)) if num <= 0])
        return out > 0

    def check_walls(self, position):
        """Проверяет, является ли position стеной.

        :param position: координаты, которые необходимо проверить
        :type position: numpy 1D array
        :return: True, если position - стена, False - иначе
        :rtype: bool
        """
        return self.maze[tuple(position)] == 1

    @property
    def valid(self):
        """
        Проверяет, является ли ситуация валидным (не является стеной или
        не выходит за пределы лабиринта).

        :return: True, если ситуация валидно, False - иначе
        :rtype: bool
        """
        if self.check_boundaries(self.position):
            return False
        elif self.check_walls(self.position):
            return False
        return True

    @property
    def finished(self):
        """
        Проверяет, является ли ситуация целевым (текущая позиция совпадает с
        целевой позицией).

        :return: True, если ситуация целевое, False - иначе
        :rtype: bool
        """
        return (self.position == self.goal).all()

    @plotlive
    def draw(self):
        """
        Рисует ситуация лабиринта.

        :return: None
        :rtype: None
        """
        plt.imshow(self.maze, interpolation="none", aspect="equal", cmap="Greys")

        plt.xticks([], [])
        plt.yticks([], [])

        ax.plot(self.goal[1], self.goal[0], "bs", markersize=4)  # Отметка цели
        ax.plot(
            self.position[1], self.position[0], "rs", markersize=4
        )  # Отметка стартовой позиции

    def __eq__(self, value: "Situation") -> bool:
        return (self.position == value.position).all()

    def __hash__(self) -> int:
        return hash(tuple(self.position))

    def __lt__(self, value: "Situation") -> int:
        return np.linalg.norm(self.position - self.goal) < np.linalg.norm(
            value.position - value.goal
        )


action_map = {0: [0, 1], 1: [1, 0], 2: [-1, 0], 3: [0, -1]}


def make_move(situation: Situation, action: int) -> Situation:
    """
    Создаёт новую ситуацию, соответствующее действию action, примененному к ситуации situation.

    :param situation: текущяя ситуация
    :type situation: Situation
    :param action: действие, которое необходимо выполнить
    :type action: int
    :return: новая ситуация, получившееся в результате действия
    :rtype: Situation
    """
    current_position = situation.position

    move = action_map[action]

    next_position = current_position + np.asarray(move)

    return Situation(situation.maze, next_position, situation.goal)
