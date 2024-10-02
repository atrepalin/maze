from maze.environment import State, make_move


# Функция поиска с использованием метода ветвей и границ
def bnb(initial_state: State):
    best_solution = None  # Инициализация лучшего решения как None
    best_cost = float("inf")  # Инициализация лучшей стоимости как бесконечность
    visited = set()  # Множество для хранения посещённых состояний

    # Вспомогательная рекурсивная функция для исследования всех возможных путей
    def explore(state: State, path, cost):
        nonlocal best_solution, best_cost

        # Если текущая стоимость превышает лучшую найденную, прекращаем исследование
        if cost >= best_cost:
            return

        # Проверяем, достигнуто ли целевое состояние
        if state.finished:
            best_solution = path  # Обновляем лучшее решение
            best_cost = cost  # Обновляем минимальную стоимость
            return

        # Если текущее состояние уже посещено, выходим из функции
        if state in visited:
            return

        # Добавляем текущее состояние в посещённые
        visited.add(state)

        # Генерируем все возможные действия (0-3)
        for action in range(4):
            next_state = make_move(state, action)

            # Если следующее состояние валидно, продолжаем его исследовать
            if next_state and next_state.valid:
                # Рекурсивно вызываем explore для следующего состояния
                explore(next_state, path + [action], cost + 1)

        # Удаляем текущее состояние из посещённых после его исследования
        visited.remove(state)

    # Запускаем исследование с начального состояния
    explore(initial_state, [], 0)

    return best_solution  # Возвращаем лучшее найденное решение
