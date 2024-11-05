from typing import List, Optional

from analyzer.statistic import Statistic
from maze.environment import Situation, make_move


# Функция поиска в глубину
def dfs_with_cmp(initial_situation: Situation) -> Optional[tuple[List[int], Statistic]]:
    """
    :param initial_situation: начальное ситуация лабиринта
    :return: список действий, приводящих к цели, или None, если решение не найдено

    Функция поиска решения в лабиринте с использованием алгоритма поиска в глубину (DFS)
    с приоритетом действий, приближающих робота к цели.

    Алгоритм работает следующим образом:
    1. Инициализируем стек, где каждый элемент представляет текущее ситуация и путь,
       приведший к нему.
    2. Проверяем, достигнуто ли целевое ситуация — если да, возвращаем путь.
    3. Добавляем текущее ситуация в множество посещённых.
    4. Генерируем возможные действия (0-3), сортируя их по эвристике, которая приближает
       робота к цели.
    5. Для каждого действия:
       - Если следующее ситуация валидно и ещё не посещено, добавляем его в стек с обновлённым путём.
    6. Если решение не найдено, возвращаем None.
    """
    visited = set()  # Храним все посещённые ситуации
    stack = [
        (initial_situation, [], 0)
    ]  # Каждый элемент: (текущее ситуация, путь действий)

    max_depth = 0  # Максимальная глубина поиска
    all_generated = 0  # Общее число порождённых вершин

    while stack:
        current_situation, path, depth = stack.pop()

        # Проверяем, достигнуто ли целевое ситуация
        if current_situation.finished:
            return path, Statistic(len(path), max_depth + 1, all_generated)

        # Добавляем текущее ситуация в посещённые
        visited.add(current_situation)
        all_generated += 1

        # Обновляем максимальную глубину
        max_depth = max(max_depth, depth)

        # Генерируем все возможные действия (0-3)
        next_actions = list(range(4))

        # Сортируем возможные действия так, чтобы робот был ближе к цели
        next_actions.sort(key=lambda action: make_move(current_situation, action))

        for action in next_actions:
            next_situation = make_move(current_situation, action)

            # Если новое ситуация валидно и не посещено ранее
            if (
                next_situation
                and next_situation.valid
                and next_situation not in visited
            ):
                # Добавляем новое ситуация в стек с обновлённым путём
                stack.append((next_situation, path + [action], depth + 1))

    return None  # Решение не найдено
