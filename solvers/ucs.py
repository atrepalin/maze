from heapq import heappop, heappush
from maze.environment import State, make_move


# Функция поиска с использованием стратегии равных цен
def ucs(initial_state: State):
    queue = [(0, initial_state, [])]
    visited = set()

    while queue:
        cost, current_state, path = heappop(queue)

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
                # Добавляем новое состояние в очередь с обновлённым путём
                heappush(queue, (cost + 1, next_state, path + [action]))

    return None  # Решение не найдено
