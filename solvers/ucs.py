from heapq import heappop, heappush
from typing import List, Optional

from analyzer.statistic import Statistic
from maze.environment import Situation, make_move


# Функция поиска с использованием стратегии равных цен
def ucs(initial_situation: Situation) -> Optional[tuple[List[int], Statistic]]:
    """
    :param initial_situation: начальное ситуация лабиринта
    :return: список действий, ведущих к цели, или None, если решение не найдено

    Функция поиска решения в лабиринте с использованием алгоритма поиска по стратегии равных цен (Uniform Cost Search, UCS).

    UCS — это вариант поиска по графу, где для каждой вершины учитывается стоимость пути от начальной точки.
    В данном случае все переходы имеют одинаковую стоимость.

    Алгоритм работает следующим образом:
    1. Инициализируем приоритетную очередь, в которой каждый элемент представляет текущую стоимость, ситуация и путь.
    2. Извлекаем ситуация с наименьшей стоимостью из очереди.
    3. Проверяем, достигнуто ли целевое ситуация — если да, возвращаем путь.
    4. Добавляем текущее ситуация в множество посещённых.
    5. Генерируем возможные действия (0-3) и для каждого действия:
       - Если следующее ситуация валидно и не посещено ранее, добавляем его в очередь с обновлённой стоимостью и путём.
    6. Если решение не найдено, возвращаем None.
    """
    queue = [
        (0, initial_situation, [], 0)
    ]  # Очередь с приоритетом (стоимость, ситуация, путь, глубина)
    visited = set()  # Множество для хранения посещённых ситуаций

    max_depth = 0  # Максимальная глубина поиска
    all_generated = 0  # Общее число порождённых вершин

    while queue:
        cost, current_situation, path, depth = heappop(
            queue
        )  # Извлекаем ситуация с наименьшей стоимостью

        # Проверяем, достигнуто ли целевое ситуация
        if current_situation.finished:
            return path, Statistic(len(path), max_depth + 1, all_generated)

        # Добавляем текущее ситуация в посещённые
        visited.add(current_situation)
        all_generated += 1

        # Обновляем максимальную глубину
        max_depth = max(max_depth, depth)

        # Генерируем все возможные действия (0-3)
        for action in range(4):
            next_situation = make_move(current_situation, action)

            # Если следующее ситуация валидно и не посещено ранее
            if (
                next_situation
                and next_situation.valid
                and next_situation not in visited
            ):
                # Добавляем новое ситуация в очередь с обновлённым путём
                heappush(queue, (cost + 1, next_situation, path + [action], depth + 1))

    return None  # Решение не найдено
