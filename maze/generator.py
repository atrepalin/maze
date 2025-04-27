# Генератор случайного лабиринта с использованием алгоритма поиска в глубину
# Источник: http://en.wikipedia.org/wiki/Maze_generation_algorithm

import random
import numpy as np


def generate(w: int = 10, h: int = 10, num_paths: int = 3) -> np.ndarray:
    """
    Генерирует случайный лабиринт с помощью алгоритма поиска в глубину с несколькими путями.

    :type w: int
    :param w: ширина лабиринта
    :type h: int
    :param h: высота лабиринта
    :type num_paths: int
    :param num_paths: количество путей в лабиринте
    :return: сгенерированный лабиринт в виде матрицы NumPy,
             где 0 - путь, 1 - стена
    :rtype: numpy 2D array
    """
    maze = [[1 for _ in range(w)] for _ in range(h)]  # Все ячейки — стены

    # Направления движения: вверх, вправо, вниз, влево
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    def carve_path(cx, cy):
        """Прокладывает путь из текущей позиции в случайном направлении."""
        stack = [(cx, cy)]  # Стек для отслеживания пути
        maze[cy][cx] = 0  # Начальная ячейка — путь

        while stack:
            x, y = stack[-1]
            directions = random.sample(range(4), 4)  # Случайный порядок направлений

            for i in directions:
                nx, ny = x + dx[i], y + dy[i]

                # Проверяем, что соседняя ячейка в пределах лабиринта и не посещена
                if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] == 1:
                    # Проверяем соседей на наличие стены
                    wall_count = 0
                    for j in range(4):
                        ex, ey = nx + dx[j], ny + dy[j]
                        if 0 <= ex < w and 0 <= ey < h and maze[ey][ex] == 0:
                            wall_count += 1
                    if wall_count == 1:  # Если у соседа только одна проходимая ячейка
                        maze[ny][nx] = 0  # Прокладываем путь
                        stack.append((nx, ny))  # Добавляем в стек
                        break
            else:
                stack.pop()  # Возвращаемся назад, если нет доступных направлений

    # Генерируем несколько путей
    for _ in range(num_paths):
        cx, cy = random.randint(0, w - 1), random.randint(0, h - 1)
        carve_path(cx, cy)

    # Преобразуем список в массив NumPy для удобства работы
    maze = np.array(maze)

    # Устанавливаем начальную и конечную точки как проходимые (0)
    maze[0][0] = 0
    maze[w - 1][h - 1] = 0

    return maze  # Возвращаем сгенерированный лабиринт


def save(maze: np.ndarray, filename: str):
    """
    Сохраняет лабиринт в файл filename.

    :type maze: numpy 2D array
    :param maze: лабиринт в виде матрицы NumPy
    :type filename: string
    :param filename: имя файла, в который будет сохранён лабиринт
    """
    np.save(filename, maze)


def load(filename: str) -> np.ndarray:
    """
    Загружает лабиринт из файла filename.

    :type filename: string
    :param filename: имя файла, из которого будет загружен лабиринт
    :return: лабиринт в виде матрицы NumPy
    :rtype: numpy 2D array
    """
    return np.load(filename)


if __name__ == "__main__":
    w, h = map(int, input("Введите ширину и высоту лабиринта: ").split())
    num_paths = int(input("Введите количество путей: "))
    filename = input("Введите имя файла: ")

    maze = generate(w, h, num_paths)

    save(maze, filename)
