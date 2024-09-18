from collections import deque

from maze.environment import State, make_move


def bfs(state: State):
    queue = deque([(state, [], [])])  # (текущее состояние, путь, действия)
    visited = set()  # Для отслеживания посещенных состояний

    while queue:
        current_state, path, actions = queue.popleft()

        position = tuple(current_state.position)

        if not current_state.valid or position in visited:
            continue

        visited.add(position)
        path.append(position)

        if current_state.finished:
            return path, actions

        for action in range(4):  # Проверяем все возможные движения
            next_state = make_move(current_state, action)
            queue.append((next_state, path.copy(), actions + [action]))

    return None
