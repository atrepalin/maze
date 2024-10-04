from collections import deque
from typing import List, Optional

from maze.environment import State, make_move


# Функция поиска в ширину
def bfs(initial_state: State) -> Optional[List[int]]:
    """
    Функция поиска в ширину (Breadth-First Search, BFS).

    Берётся начальное состояние и строится дерево с помощью очереди,
    где каждый узел - это состояние, а каждый ребро - это действие,
    которое привело к этому состоянию.

    Алгоритм работает следующим образом:
    1. Инициализируем очередь, содержащую начальное состояние.
    2. Берём верхний элемент очереди, это текущее состояние.
    3. Если текущее состояние - это целевое, то возвращаем путь,
       который привёл к этому состоянию.
    4. Иначе, генерируем все возможные действия (0-3) и
       добавляем в очередь новые состояния, полученные из текущего,
       с обновлённым путём.
    5. Если очередь пуста, то решение не найдено.

    :param initial_state: начальное состояние
    :return: путь, который привёл к целевому состоянию, или None,
             если решение не найдено
    """
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
