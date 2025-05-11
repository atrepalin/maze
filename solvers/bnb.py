from heapq import heappop, heappush
from typing import List, Optional

from analyzer.statistic import Statistic
from maze.environment import Situation, make_move


# Функция поиска с использованием метода ветвей и границ
def bnb(initial_situation: Situation) -> Optional[tuple[List[int], Statistic]]:
    """
    :param initial_situation: начальная ситуация лабиринта
    :return: список действий, ведущих к цели, или None, если решение не найдено

    Функция поиска с использованием метода ветвей и границ (Branch and Bound, BnB).

    Алгоритм работает следующим образом:
    1. Инициализируем приоритетную очередь, в которой каждый элемент представляет текущую стоимость, ситуацию и путь.
    2. Извлекаем ситуацию с наименьшей стоимостью из очереди.
    3. Проверяем, достигнуто ли целевая ситуация — если да, возвращаем путь.
    4. Добавляем текущую ситуацию в множество посещённых.
    5. Генерируем возможные действия (0-3) и для каждого действия:
       - Если следующая ситуация валидна и не посещена ранее, добавляем её в очередь с обновлённой стоимостью и путём.
    6. Если решение не найдено, возвращаем None.
    """
    queue = [
        (initial_situation.heuristic(), initial_situation, [], 0)
    ]  # Очередь с приоритетом (стоимость, ситуация, путь, глубина)
    visited = set()  # Множество для хранения посещённых ситуаций

    max_depth = 0  # Максимальная глубина поиска
    all_generated = 0  # Общее число порождённых вершин

    while queue:
        _, current_situation, path, depth = heappop(
            queue
        )  # Извлекаем ситуацию с наименьшей стоимостью

        # Проверяем, достигнута ли целевая ситуация
        if current_situation.finished:
            return path, Statistic(len(path), max_depth + 1, all_generated)

        # Добавляем текущую ситуацию в посещённые
        visited.add(current_situation)
        all_generated += 1

        # Обновляем максимальную глубину
        max_depth = max(max_depth, depth)

        # Генерируем все возможные действия (0-3)
        for action in range(4):
            next_situation = make_move(current_situation, action)

            # Если следующая ситуация валидна и не посещена ранее
            if (
                next_situation
                and next_situation.valid
                and next_situation not in visited
            ):
                cost = next_situation.heuristic()

                # Добавляем новую ситуацию в очередь с обновлённым путём
                heappush(queue, (cost, next_situation, path + [action], depth + 1))

    return None  # Решение не найдено
