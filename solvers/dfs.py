from maze.environment import State, make_move


def dfs(state: State, path: list = [], actions: list = []):
    position = tuple(state.position)

    if not state.valid or position in path:
        return None

    path.append(position)

    if state.finished:
        return path, actions

    for action in range(4):  # Проверяем все возможные движения
        next_state = make_move(state, action)
        result = dfs(next_state, path, actions + [action])
        if result is not None:
            return result

    path.pop()  # Возврат, если путь не найден
    return None
