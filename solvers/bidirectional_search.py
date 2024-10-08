from collections import deque
from typing import Dict, List, Tuple
from maze.environment import State, make_move


def bidirectional_search(initial_state: State, goal_state: State):
    """
    Алгоритм двунаправленного поиска для нахождения пути от начального состояния к целевому.

    :param initial_state: начальное состояние робота в лабиринте
    :param goal_state: целевое состояние (финиш)
    :return: список действий, ведущих к цели, или None, если решение не найдено
    """
    # Очереди для двух направлений поиска
    front_queue = deque([(initial_state, [])])  # Поиск от начального состояния
    back_queue = deque([(goal_state, [])])  # Поиск от целевого состояния

    # Множества для посещённых состояний с каждой стороны
    front_visited = {
        initial_state: []
    }  # Карта: состояние -> путь от начального состояния
    back_visited = {goal_state: []}  # Карта: состояние -> путь от целевого состояния

    while front_queue and back_queue:
        # Расширяем фронт от начального состояния
        result = expand_front(front_queue, front_visited, back_visited, False)
        if result:
            return result  # Путь найден

        # Расширяем фронт от целевого состояния
        result = expand_front(back_queue, back_visited, front_visited, True)
        if result:
            return result  # Путь найден

    return None  # Решение не найдено


def expand_front(
    queue: deque[Tuple[State, List]],
    visited_from_this_side: Dict[State, List],
    visited_from_other_side: Dict[State, List],
    reverse_path: bool,
):
    """
    Расширяет один фронт поиска и проверяет пересечение с другим фронтом.

    :param queue: очередь для текущего фронта поиска
    :param visited_from_this_side: состояния, посещённые с этой стороны
    :param visited_from_other_side: состояния, посещённые с противоположной стороны
    :param reverse_path: если True, разворачиваем путь от целевого состояния
    :return: список действий, если путь найден, или None
    """
    current_state, path = queue.popleft()

    # Проверяем, пересекается ли текущее состояние с другим фронтом
    if current_state in visited_from_other_side:
        # Получаем путь от другого фронта
        other_path = visited_from_other_side[current_state]

        # Если мы расширяем путь от целевого состояния, разворачиваем его
        if reverse_path:
            return path + [
                (3 - x) for x in other_path[::-1]
            ]  # Объединяем путь от начального и целевого состояния
        else:
            return (
                other_path[::-1] + path
            )  # Объединяем путь от начального и целевого состояния

    # Генерируем возможные действия (0-3) и продолжаем исследование
    for action in range(4):
        next_state = make_move(current_state, action)

        # Если следующее состояние валидно и не посещено с этой стороны
        if next_state and next_state.valid and next_state not in visited_from_this_side:
            visited_from_this_side[next_state] = path + [action]  # Обновляем путь
            queue.append((next_state, path + [action]))

    return None
