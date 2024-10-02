from typing import List, Optional
from maze.environment import State, make_move


# Функция поиска в глубину
def dfs(initial_state: State) -> Optional[List[int]]:
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
        for action in range(4):
            next_state = make_move(current_state, action)

            # Если новое состояние валидно и не посещено ранее
            if next_state and next_state.valid and next_state not in visited:
                # Добавляем новое состояние в стек с обновлённым путём
                stack.append((next_state, path + [action]))

    return None  # Решение не найдено
