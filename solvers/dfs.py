from typing import List, Optional
from maze.environment import State, make_move


# Функция поиска в глубину
def dfs(initial_state: State) -> Optional[List[int]]:
    """
    Функция поиска в глубину (Depth-First Search, DFS).

    Берётся начальное состояние и строится дерево с помощью стека,
    где каждый узел - это состояние, а каждый ребро - это действие,
    которое привело к этому состоянию.

    Алгоритм работает следующим образом:
    1. Инициализируем стек, содержащий начальное состояние.
    2. Берём верхний элемент стека, это текущее состояние.
    3. Если текущее состояние - это целевое, то возвращаем путь,
       который привёл к этому состоянию.
    4. Иначе, генерируем все возможные действия (0-3) и
       добавляем в стек новые состояния, полученные из текущего,
       с обновлённым путём.
    5. Если стек пуст, то решение не найдено.

    :param initial_state: начальное состояние
    :return: путь, который привёл к целевому состоянию, или None,
             если решение не найдено
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
        for action in range(4):
            next_state = make_move(current_state, action)

            # Если новое состояние валидно и не посещено ранее
            if next_state and next_state.valid and next_state not in visited:
                # Добавляем новое состояние в стек с обновлённым путём
                stack.append((next_state, path + [action]))

    return None  # Решение не найдено
