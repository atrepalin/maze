from typing import List, Optional
from maze.environment import State, make_move


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

        # Генерируем все возможные действия (0-3)
        next_actions = list(range(4))

        # Сортируем возможные действия так, чтобы робот был ближе к цели
        next_actions.sort(key=lambda action: make_move(current_state, action))

        for action in next_actions:
            next_state = make_move(current_state, action)

            # Если новое состояние валидно и не посещено ранее
            if next_state and next_state.valid and next_state not in visited:
                # Добавляем новое состояние в стек с обновлённым путём
                stack.append((next_state, path + [action]))

    return None  # Решение не найдено
