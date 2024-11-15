from typing import List, Optional

from analyzer.statistic import Statistic
from maze.environment import Situation, make_move


# Функция поиска с использованием метода ветвей и границ
def bnb(initial_situation: Situation) -> Optional[tuple[List[int], Statistic]]:
    """
    :param initial_situation: начальное ситуация
    :return: путь, который привёл к целевой ситуации, или None,
             если решение не найдено

    Функция поиска с использованием метода ветвей и границ (Branch and Bound, BnB).

    Берётся начальная ситуация и строится дерево с помощью рекурсивной функции,
    где каждый узел - это ситуация, а каждый ребро - это действие,
    которое привело к этой ситуации.

    Алгоритм работает следующим образом:
    1. Инициализируем лучшее решение как None и лучшую стоимость как бесконечность.
    2. Вспомогательная рекурсивная функция explore исследует все возможные пути,
       начиная с начальной ситуации.
    3. Если текущая стоимость превышает лучшую найденную, прекращаем исследование.
    4. Если достигнута целевая ситуация, обновляем лучшее решение и минимальную стоимость.
    5. Если текущая ситуация уже посещено, выходим из функции.
    6. Генерируем все возможные действия (0-3) и рекурсивно вызываем explore
       для следующей ситуации.
    7. Удаляем текущую ситуацию из посещённых после её исследования.
    8. Возвращаем лучшее найденное решение.
    """

    best_solution = None
    best_cost = float("inf")
    visited = set()
    max_depth = 0
    all_generated = 0

    def explore(situation: Situation, path, cost, depth):
        nonlocal best_solution, best_cost, max_depth, all_generated

        if cost >= best_cost:
            return

        if situation.finished:
            best_solution = path
            best_cost = cost
            return

        if situation in visited:
            return

        visited.add(situation)
        all_generated += 1
        max_depth = max(max_depth, depth)

        for action in range(4):
            next_situation = make_move(situation, action)

            if next_situation and next_situation.valid:
                explore(next_situation, path + [action], cost + 1, depth + 1)

        visited.remove(situation)

    explore(initial_situation, [], 0, 0)

    if best_solution is not None:
        return best_solution, Statistic(
            len(best_solution), max_depth + 1, all_generated
        )
    else:
        return None
