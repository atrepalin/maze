from abc import ABC


class AbstractState(ABC):
    @property
    def valid(self) -> bool:
        return False

    @property
    def finished(self) -> bool:
        return False

    def draw(self):
        pass

    def __eq__(self, value: "AbstractState") -> bool:
        return False

    def __lt__(self, value: "AbstractState") -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def make_move(self, action: int) -> "AbstractState":
        pass

    @property
    def actions(self) -> int:
        return 0
