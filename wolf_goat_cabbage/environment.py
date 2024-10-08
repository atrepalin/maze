from copy import deepcopy
from enum import Enum, Flag, auto
from typing import List, Optional
from collections import deque


# Определения перечислений и классов
class Coast(Enum):
    LEFT = "Левый"
    RIGHT = "Правый"


class Entity(Flag):
    WOLF = auto()
    GOAT = auto()
    CABBAGE = auto()


# Сущности
entities = [Entity.WOLF, Entity.GOAT, Entity.CABBAGE]


class State:
    def __init__(self, left: Entity, right: Entity, boat: Entity, coast: Coast):
        self.left = left  # Левый берег (содержит сущности, находящиеся на левом берегу)
        self.right = (
            right  # Правый берег (содержит сущности, находящиеся на правом берегу)
        )
        self.boat = boat  # Кто находится в лодке
        self.coast = coast  # Текущий берег лодки

    # Функция проверки валидности текущей ситуации

    @property
    def valid(self):
        # Проверка для каждого берега отдельно
        def check_danger(side, boat_side):
            # Если волк и коза на одном берегу без лодки - опасно
            if (Entity.WOLF in side and Entity.GOAT in side) and (
                Entity.GOAT not in boat_side
            ):
                return False
            # Если коза и капуста на одном берегу без лодки - опасно
            if (Entity.GOAT in side and Entity.CABBAGE in side) and (
                Entity.GOAT not in boat_side
            ):
                return False
            return True

        if self.coast == Coast.LEFT:
            boat_side = self.left
        else:
            boat_side = self.right

        # Проверяем левый берег
        if not check_danger(self.left, boat_side):
            return False
        # Проверяем правый берег
        if not check_danger(self.right, boat_side):
            return False

        return True

    # Функция для отображения текущего состояния игры
    def draw(self):
        # Левый берег
        print(f"Левый берег: {self.describe(self.left)}")
        # Правый берег
        print(f"Правый берег: {self.describe(self.right)}")
        # Лодка и текущий берег
        print(f"Лодка: {self.describe(self.boat)}")
        print(f"Берег лодки: {self.coast.value}")
        print("-" * 50)

    # Вспомогательная функция для описания сущностей на берегах и в лодке
    def describe(self, entities):
        description = []
        if Entity.WOLF in entities:
            description.append("Волк")
        if Entity.GOAT in entities:
            description.append("Коза")
        if Entity.CABBAGE in entities:
            description.append("Капуста")
        return ", ".join(description) if description else "Пусто"

    # Проверка на победу (все перевезены на правый берег)
    @property
    def finished(self):
        # Если все сущности находятся на правом берегу и лодка тоже на правом
        return (
            self.left == Entity(0)
            and self.boat == Entity(0)
            and self.coast == Coast.RIGHT
        )

    # Генерация уникального ключа состояния для отслеживания посещённых состояний
    def get_key(self):
        return (self.left, self.right, self.boat, self.coast)

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash(self.get_key())

    def __lt__(self, other):
        return self.right.value > other.right.value

    # Пораждающая процедура
    def make_move(self, action: int) -> Optional["State"]:
        state = deepcopy(self)

        if action < 3:
            # Перевозим с левого берега
            if (
                state.coast == Coast.LEFT
                and entities[action] in state.left
                and state.boat == Entity(0)
            ):

                state.left &= ~entities[action]
                state.boat = entities[action]
            else:
                return None
        elif action < 6:
            # Перевозим с правого берега
            move_index = action % 3
            if (
                state.coast == Coast.RIGHT
                and entities[move_index] in state.right
                and state.boat == Entity(0)
            ):

                state.right &= ~entities[move_index]
                state.boat = entities[move_index]
            else:
                return None
        elif action == 6:
            # Перемещаем лодку на противоположный берег
            if state.coast == Coast.LEFT:
                state.coast = Coast.RIGHT
                state.right |= state.boat
            else:
                state.coast = Coast.LEFT
                state.left |= state.boat

            # После перемещения лодка пустая
            state.boat = Entity(0)
        else:
            return None  # Неверный номер действия

        return state

    @property
    def actions(self) -> int:
        return 7
