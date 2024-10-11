from collections import deque
from typing import Dict, List, Tuple
from maze.environment import Situation, make_move


def bidirectional_search(initial_situation: Situation, goal_situation: Situation):
    """
    Алгоритм двунаправленного поиска для нахождения пути от начального ситуации к целевому.

    :param initial_situation: начальное ситуация робота в лабиринте
    :param goal_situation: целевое ситуация (финиш)
    :return: список действий, ведущих к цели, или None, если решение не найдено
    """
    # Очереди для двух направлений поиска
    front_queue = deque([(initial_situation, [])])  # Поиск от начального ситуации
    back_queue = deque([(goal_situation, [])])  # Поиск от целевого ситуации

    # Множества для посещённых состояний с каждой стороны
    front_visited = {
        initial_situation: []
    }  # Карта: ситуация -> путь от начального ситуации
    back_visited = {goal_situation: []}  # Карта: ситуация -> путь от целевого ситуации

    while front_queue and back_queue:
        # Расширяем фронт от начального ситуации
        result = expand_front(front_queue, front_visited, back_visited, False)
        if result:
            return result  # Путь найден

        # Расширяем фронт от целевого ситуации
        result = expand_front(back_queue, back_visited, front_visited, True)
        if result:
            return result  # Путь найден

    return None  # Решение не найдено


def expand_front(
    queue: deque[Tuple[Situation, List]],
    visited_from_this_side: Dict[Situation, List],
    visited_from_other_side: Dict[Situation, List],
    reverse_path: bool,
):
    """
    Расширяет один фронт поиска и проверяет пересечение с другим фронтом.

    :param queue: очередь для текущего фронта поиска
    :param visited_from_this_side: ситуации, посещённые с этой стороны
    :param visited_from_other_side: ситуации, посещённые с противоположной стороны
    :param reverse_path: если True, разворачиваем путь от целевого ситуации
    :return: список действий, если путь найден, или None
    """
    current_situation, path = queue.popleft()

    # Проверяем, пересекается ли текущее ситуация с другим фронтом
    if current_situation in visited_from_other_side:
        # Получаем путь от другого фронта
        other_path = visited_from_other_side[current_situation]

        # Если мы расширяем путь от целевого ситуации, разворачиваем его
        if reverse_path:
            return path + [
                (3 - x) for x in other_path[::-1]
            ]  # Объединяем путь от начального и целевого ситуации
        else:
            return (
                other_path[::-1] + path
            )  # Объединяем путь от начального и целевого ситуации

    # Генерируем возможные действия (0-3) и продолжаем исследование
    for action in range(4):
        next_situation = make_move(current_situation, action)

        # Если следующее ситуация валидно и не посещено с этой стороны
        if next_situation and next_situation.valid and next_situation not in visited_from_this_side:
            visited_from_this_side[next_situation] = path + [action]  # Обновляем путь
            queue.append((next_situation, path + [action]))

    return None
