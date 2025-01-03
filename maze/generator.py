# Генератор случайного лабиринта с использованием алгоритма поиска в глубину
# Источник: http://en.wikipedia.org/wiki/Maze_generation_algorithm

import random
import numpy as np


def generate(w: int=10, h: int=10) -> np.ndarray:
    """
    Генерирует случайный лабиринт с помощью алгоритма поиска в глубину.

    :type w: int
    :param w: ширина лабиринта
    :type h: int
    :param h: высота лабиринта
    :return: сгенерированный лабиринт в виде матрицы NumPy,
             где 0 - путь, 1 - стена
    :rtype: numpy 2D array
    """
    maze = [[0 for _ in range(w)] for _ in range(h)]

    # Направления движения: вверх, вправо, вниз, влево
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    # Случайная стартовая позиция для генерации лабиринта
    cx = random.randint(0, w - 1)
    cy = random.randint(0, h - 1)

    # Устанавливаем начальную ячейку как проходимую (1)
    maze[cy][cx] = 1

    # Стек для хранения текущей позиции и направления
    stack = [(cx, cy, 0)]  # (x, y, направление)

    while len(stack) > 0:
        # Получаем текущую позицию и направление
        (cx, cy, cd) = stack[-1]

        # Проверяем возможность смены направления
        if len(stack) > 2:
            # Если предыдущее направление отличается от текущего,
            # то не можем сменить направление на текущем шаге
            if cd != stack[-2][2]:
                dirRange = [cd]  # Только текущее направление
            else:
                dirRange = range(4)  # Все направления
        else:
            dirRange = range(4)  # Все направления

        # Список для хранения свободных соседей
        nlst = []

        for i in dirRange:
            # Рассчитываем координаты соседней ячейки
            nx = cx + dx[i]
            ny = cy + dy[i]

            # Проверяем, что соседняя ячейка находится в пределах лабиринта
            if 0 <= nx < w and 0 <= ny < h:
                # Если ячейка ещё не посещена (0)
                if maze[ny][nx] == 0:
                    ctr = 0  # Счетчик для занятых соседей
                    for j in range(4):
                        # Проверяем соседей текущей ячейки
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if 0 <= ex < w and 0 <= ey < h:
                            if maze[ey][ex] == 1:  # Если сосед проходимый
                                ctr += 1
                    # Добавляем в список только если у соседа ровно один проходимый сосед
                    if ctr == 1:
                        nlst.append(i)

        # Если есть свободные соседи, выбираем случайного и добавляем его в стек
        if len(nlst) > 0:
            ir = nlst[
                random.randint(0, len(nlst) - 1)
            ]  # Случайный выбор из свободных соседей
            cx += dx[ir]  # Обновляем координаты
            cy += dy[ir]
            maze[cy][cx] = 1  # Устанавливаем ячейку как проходимую
            stack.append((cx, cy, ir))  # Добавляем новую позицию в стек
        else:
            stack.pop()  # Если нет свободных соседей, возвращаемся назад по стеку

    # Преобразуем список в массив NumPy для удобства работы
    maze = np.array(maze)

    # Приводим значения к нужному формату (0 - путь, 1 - стена)
    maze -= 1
    maze = abs(maze)

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
    filename = input("Введите имя файла: ")

    maze = generate(w, h)

    save(maze, filename)
