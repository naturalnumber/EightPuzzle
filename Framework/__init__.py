import math
from abc import ABCMeta, abstractmethod
from collections import Iterable

from typing import TypeVar, Callable, Any, Generic

N = TypeVar('N', int, float)

A = TypeVar('A')

D = TypeVar('D')

S = TypeVar('S')

T = TypeVar('T', Callable[[A], D], Callable[[A, D], D]) #...

def _order(i: int, j: int) -> tuple[int, int]:
    if i < j: return i, j
    else: return j, i

class AState(Generic[S], metaclass=ABCMeta):

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass

    @abstractmethod
    def __le__(self, other) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __ne__(self, other) -> bool:
        pass

    @abstractmethod
    def __gt__(self, other) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other) -> bool:
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class AAction(Generic[A], metaclass=ABCMeta):

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __int__(self) -> int:
        pass

    @abstractmethod
    def __float__(self) -> float:
        pass

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass

    @abstractmethod
    def __le__(self, other) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __ne__(self, other) -> bool:
        pass

    @abstractmethod
    def __gt__(self, other) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other) -> bool:
        pass


class ANode(Generic[D], metaclass=ABCMeta):
    parent: D

    def __init__(self, parent: D = False):
        self.parent = parent

    @abstractmethod
    def __int__(self) -> int:
        pass

    @abstractmethod
    def __float__(self) -> float:
        pass

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass

    @abstractmethod
    def __le__(self, other) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __ne__(self, other) -> bool:
        pass

    @abstractmethod
    def __gt__(self, other) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def expand(self, ignore) -> set:
        pass

    @abstractmethod
    def actions(self) -> set:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def transition(self, action):
        pass

    @abstractmethod
    def is_goal(self) -> bool:
        pass


class DelegatingState(AState[S]):
    configuration: D

    def __init__(self, configuration: S):
        self.configuration = configuration

    def __str__(self) -> str:
        return self.configuration.__str__()

    def __lt__(self, other) -> bool:
        return self.configuration.__lt__(other.state)

    def __le__(self, other) -> bool:
        return self.configuration.__le__(other.state)

    def __eq__(self, other) -> bool:
        return self.configuration.__eq__(other.state)

    def __ne__(self, other) -> bool:
        return self.configuration.__ne__(other.state)

    def __gt__(self, other) -> bool:
        return self.configuration.__gt__(other.state)

    def __ge__(self, other) -> bool:
        return self.configuration.__ge__(other.state)

    def __getitem__(self, key):
        if hasattr(self.configuration, "__getitem__") and callable(getattr(self.configuration, "__getitem__")):
            return self.configuration.__getitem__(key)
        if hasattr(self.configuration, key):
            return getattr(self.configuration, key)
        return None


class StringState(DelegatingState[str]):
    marked: int

    def __init__(self, configuration: str, marked: int = None):
        super().__init__(configuration)
        self.marked = marked

    def __str__(self) -> str:
        return self.configuration

    def __len__(self) -> int:
        return self.configuration.__len__()

    def __getitem__(self, key):
        return self.configuration.__getitem__(key)

    def swap(self, i: int, j: int = None) -> str:
        if j is None:
            if self.marked is not None:
                j = self.marked
            else:
                j = 0

        if i == j: return self.configuration

        min_i, max_i = _order(i, j)

        return self.configuration[:min_i] + self.configuration[max_i] + self.configuration[min_i + 1:max_i] \
               + self.configuration[min_i] + self.configuration[max_i + 1:]


class CharGrid(StringState):
    _rows: int
    _cols: int

    def __init__(self, configuration: str, rows: int = 0, cols: int = 0, marked: int = None):
        super().__init__(configuration, marked)

        if rows > 0 and cols > 0 and len(configuration) == rows * cols:
            self._rows = rows
            self._cols = cols

        elif rows > 0 and len(configuration) % rows == 0:
            self._rows = rows
            self._cols = len(configuration) // rows

        elif cols > 0 and len(configuration) % cols == 0:
            self._rows = len(configuration) // cols
            self._cols = cols

        elif int(math.sqrt(len(configuration)))**2 == len(configuration):
            self._rows = rows
            self._cols = cols

        else:
            raise AttributeError(configuration, rows, cols)

    def __getitem__(self, key):
        if type(key) is tuple and len(key) == 2:
            key: tuple
            return self.get(*key)
        return super().__getitem__(key)

    def __str__(self) -> str:
        string: str = ""
        for i in range(self._rows):
            string += self.get_row(i) + '\n'
        return string

    def coord(self, i: int) -> tuple[int, int]:
        if i > self._rows * self._cols - 1: raise IndexError(i)
        return i // self._cols, i % self._cols

    def _flat(self, i: int, j: int) -> int:
        if i > self._rows or j > self._cols: raise IndexError(i, j)
        return i * self._cols + j

    def get(self, i: int, j: int) -> str:
        return self.configuration[self._flat(i, j)]

    def get_row(self, i: int) -> str:
        return self.configuration[self._flat(i, 0):self._flat(i + 1, 0)]

    def get_col(self, j: int) -> str:
        string: str = ""
        for i in range(self._rows):
            string += self.configuration[self._flat(i, j)]
        return string

    def swap(self, i, j=None) -> str:
        if type(i) is tuple:
            i: tuple
            if type(j) is tuple:
                j: tuple
                return super().swap(self._flat(*i), self._flat(*j))
            return super().swap(self._flat(*i), j)
        return super().swap(i, j)

class Action(AAction[A]):
    name: str
    cost: N
    transform: Callable #further hints
    target: A
    result: A

    def __init__(self, name: str, cost: N = 1, transform: Callable = None, target: A = None, result: A = False):
        self.name = name
        self.cost = cost

        if result and transform: raise AttributeError(transform, result)

        self.transform = transform

        self.target = target
        self.result = result

    def __str__(self) -> str:
        string: str = self.name

        if self.target or self.cost != 1 or self.result:
            string += ":"

        if self.transform: string += " ." + str(self.transform) + "()"
        if self.target: string += " " + self.target.name() ## Clean this name stuff up
        if self.cost != 1: string += f" -{self.cost}->"
        if self.result: string += " " + self.result.name()

        return string

    def __int__(self) -> int:
        if type(self.cost) is int: return self.cost
        return int(self.cost)

    def __float__(self) -> float:
        if type(self.cost) is float: return self.cost
        return float(self.cost)

    def __lt__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost < int(other)
        return self.cost < float(other)

    def __le__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost <= int(other)
        return self.cost <= float(other)

    def __eq__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost == int(other)
        return self.cost == float(other)

    def __ne__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost != int(other)
        return self.cost != float(other)

    def __gt__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost > int(other)
        return self.cost > float(other)

    def __ge__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost >= int(other)
        return self.cost >= float(other)


class CostNode(ANode[D], metaclass=ABCMeta):
    action: Action[D]
    cost: N
    _actions: set[Action[D]]
    _children: set[D]
    _expanded: bool
    _examined: bool

    def __init__(self, parent: D = None, action: Action[D] = None, cost: N = 0):
        super().__init__(parent)

        self.action = action
        self.cost = cost

        self._actions = set()
        self._children = set()

        self._expanded = False
        self._examined = False

    def __int__(self) -> int:
        if type(self.cost) is int: return self.cost
        return int(self.cost)

    def __float__(self) -> float:
        if type(self.cost) is float: return self.cost
        return float(self.cost)

    def __lt__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost < int(other)
        return self.cost < float(other)

    def __le__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost <= int(other)
        return self.cost <= float(other)

    def __eq__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost == int(other)
        return self.cost == float(other)

    def __ne__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost != int(other)
        return self.cost != float(other)

    def __gt__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost > int(other)
        return self.cost > float(other)

    def __ge__(self, other) -> bool:
        if type(self.cost) is int:
            return self.cost >= int(other)
        return self.cost >= float(other)

    def __getitem__(self, key: Action):
        if type(key) is Action: return self.transition(key)
        return None


class StateNode(CostNode[D], metaclass=ABCMeta):
    state: AState[S] #????
    _transitions: dict[Action[D], Any] # Further type hints

    def __init__(self, state: AState[S], parent: CostNode = None, action: Action = None, cost: N = 0,
                 transitions: dict = None):
        super().__init__(parent, action, cost)

        self.state = state

        self._transitions = transitions

    def expand(self, ignore: Iterable[D]=None) -> set[D]:
        if not self._expanded:
            if ignore:
                self._children = {x for x in self._generate_children() if x not in ignore}
            else:
                self._children = self._generate_children()
            self._expanded = True
        return self._children

    def actions(self) -> set[Action[D]]:
        if not self._examined:
            self._actions = self._generate_actions()
            self._examined = True
        return self._actions

    # May need to override

    def __getitem__(self, key):
        if type(key) is Action: return super().__getitem__(key)
        return self.state.__getitem__(key)

    def __str__(self) -> str:
        return self.state.__str__()

    def _generate_children(self) -> set[D]:
        return {self.transition(x) for x in self.actions()}

    def name(self) -> str:
        return self.state.__str__()

    def transition(self, action: Action[D]) -> D:
        if self._transitions:
            if self._transitions[action]:
                if callable(self._transitions[action]):
                    return self._transitions[action](source=self)
                else:
                    return self._transitions[action]
        elif action.result:
            return action.result
        elif action.transform:
            return action.transform(source=self, action=action)
        else:
            raise KeyError(action)

    # Must override

    @abstractmethod
    def _generate_actions(self) -> set:
        pass
