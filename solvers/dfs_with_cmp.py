from typing import Callable, List, Optional
import numpy as np
from maze.environment import State, make_move
from functools import cmp_to_key


def distance(state: State):
    return np.linalg.norm(state.position - state.goal)


# Функция поиска в глубину
def dfs_with_cmp(
    initial_state: State, rate: Callable[[State], float]
) -> Optional[List[int]]:
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

        comparator = lambda x, y: rate(make_move(initial_state, x)) - rate(
            make_move(initial_state, y)
        )

        next_actions.sort(key=cmp_to_key(comparator))

        for action in next_actions:
            next_state = make_move(current_state, action)

            # Если новое состояние валидно и не посещено ранее
            if next_state and next_state.valid and next_state not in visited:
                # Добавляем новое состояние в стек с обновлённым путём
                stack.append((next_state, path + [action]))

    return None  # Решение не найдено
