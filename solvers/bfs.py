from collections import deque
from typing import List, Optional

from maze.environment import State, make_move


# Функция поиска в ширину
def bfs(initial_state: State) -> Optional[List[int]]:
    visited = set()  # Храним все посещённые состояния
    queue = deque(
        [(initial_state, [])]
    )  # Каждый элемент: (текущее состояние, путь действий)

    while queue:
        current_state, path = queue.popleft()

        # Проверяем, достигнуто ли целевое состояние
        if current_state.finished:
            return path

        # Пропускаем, если это состояние уже было посещено
        if current_state in visited:
            continue

        # Добавляем текущее состояние в посещённые
        visited.add(current_state)

        # Генерируем все возможные действия (0-3)
        for action in range(4):
            next_state = make_move(current_state, action)

            # Если новое состояние валидно и не посещено ранее
            if next_state and next_state.valid and next_state not in visited:
                # Добавляем новое состояние в очередь с обновлённым путём
                queue.append((next_state, path + [action]))

    return None  # Решение не найдено
