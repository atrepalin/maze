from typing import List, Optional
from maze.environment import Situation, make_move


# Функция поиска в глубину
def dfs(initial_situation: Situation) -> Optional[List[int]]:
    """
    Функция поиска в глубину (Depth-First Search, DFS).

    Берётся начальное ситуация и строится дерево с помощью стека,
    где каждый узел - это ситуация, а каждый ребро - это действие,
    которое привело к этому состоянию.

    Алгоритм работает следующим образом:
    1. Инициализируем стек, содержащий начальное ситуация.
    2. Берём верхний элемент стека, это текущее ситуация.
    3. Если текущее ситуация - это целевое, то возвращаем путь,
       который привёл к этому состоянию.
    4. Иначе, генерируем все возможные действия (0-3) и
       добавляем в стек новые ситуации, полученные из текущего,
       с обновлённым путём.
    5. Если стек пуст, то решение не найдено.

    :param initial_situation: начальное ситуация
    :return: путь, который привёл к целевому состоянию, или None,
             если решение не найдено
    """
    visited = set()  # Храним все посещённые ситуации
    stack = [(initial_situation, [])]  # Каждый элемент: (текущее ситуация, путь действий)

    while stack:
        current_situation, path = stack.pop()

        # Проверяем, достигнуто ли целевое ситуация
        if current_situation.finished:
            return path

        # Добавляем текущее ситуация в посещённые
        visited.add(current_situation)

        # Генерируем все возможные действия (0-3)
        for action in range(4):
            next_situation = make_move(current_situation, action)

            # Если новое ситуация валидно и не посещено ранее
            if next_situation and next_situation.valid and next_situation not in visited:
                # Добавляем новое ситуация в стек с обновлённым путём
                stack.append((next_situation, path + [action]))

    return None  # Решение не найдено
