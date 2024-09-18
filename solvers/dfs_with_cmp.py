from typing import Callable
import numpy as np
from maze.environment import State, make_move
from functools import cmp_to_key


def distance(state: State):
    return np.linalg.norm(state.position - state.goal)


def dfs_with_cmp(
    state: State, rate: Callable[[State], float], path: list = [], actions: list = []
):
    position = tuple(state.position)

    if not state.valid or position in path:
        return None

    path.append(position)

    if state.finished:
        return path, actions

    next_actions = list(range(4))

    comparator = lambda x, y: rate(make_move(state, x)) - rate(make_move(state, y))

    next_actions.sort(key=cmp_to_key(comparator))

    for action in next_actions:  # Проверяем все возможные движения
        next_state = make_move(state, action)
        result = dfs_with_cmp(next_state, rate, path, actions + [action])
        if result is not None:
            return result

    path.pop()  # Возврат, если путь не найден
    return None
