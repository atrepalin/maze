from functools import cmp_to_key
from typing import List, Optional
from maze.environment import State


# Функция поиска в глубину
def dfs_with_cmp(initial_state: State) -> Optional[List[int]]:
    """
    Функция поиска решения в лабиринте с использованием алгоритма поиска в глубину (DFS)
    с приоритетом действий, приближающих робота к цели.

    Алгоритм работает следующим образом:
    1. Инициализируем стек, где каждый элемент представляет текущее состояние и путь,
       приведший к нему.
    2. Проверяем, достигнуто ли целевое состояние — если да, возвращаем путь.
    3. Добавляем текущее состояние в множество посещённых.
    4. Генерируем возможные действия (0-3), сортируя их по эвристике, которая приближает
       робота к цели.
    5. Для каждого действия:
       - Если следующее состояние валидно и ещё не посещено, добавляем его в стек с обновлённым путём.
    6. Если решение не найдено, возвращаем None.

    :param initial_state: начальное состояние лабиринта
    :return: список действий, приводящих к цели, или None, если решение не найдено
    """
    visited = set()  # Храним все посещённые состояния
    stack = [(initial_state, [])]  # Каждый элемент: (текущее состояние, путь действий)

    while stack:
        current_state, path = stack.pop()

        # Проверяем, достигнуто ли целевое состояние
        if current_state.finished:
            return path

        # Добавляем текущее состояние в посещённые
        visited.add(current_state)

        # Генерируем все возможные действия
        next_actions = list(range(current_state.actions))

        def cmp(a, b):
            a_state = current_state.make_move(a)
            b_state = current_state.make_move(b)

            if a_state is None:
                return 1
            elif b_state is None:
                return -1
            elif a_state == b_state:
                return 0
            else:
                return -1 if a_state < b_state else 1

        # Сортируем возможные действия так, чтобы робот был ближе к цели
        next_actions.sort(key=cmp_to_key(cmp))

        for action in next_actions:
            next_state = current_state.make_move(action)

            # Если новое состояние валидно и не посещено ранее
            if next_state and next_state.valid and next_state not in visited:
                # Добавляем новое состояние в стек с обновлённым путём
                stack.append((next_state, path + [action]))

    return None  # Решение не найдено
