import math
from abc import ABCMeta, abstractmethod
from collections import Iterable
# from __future__ import annotations

from typing import TypeVar, Callable, Generic, Any

N = TypeVar('N', int, float)  # Number

A = TypeVar('A')  # Action

D = TypeVar('D')  # Node

S = TypeVar('S')  # State

C = TypeVar('C')  # Configuration


# T = TypeVar('T', Callable[[A], D], Callable[[A, D], D]) #...

def _order(i: int, j: int) -> tuple:
    if i < j: return i, j
    else: return j, i


class AState(Generic[S, C], metaclass=ABCMeta):

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


class AAction(Generic[A, S], metaclass=ABCMeta):

    @abstractmethod
    def __str__(self) -> str:
        pass


class AEdge(Generic[D], metaclass=ABCMeta):

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


class DelegatingState(AState[S, C]):
    configuration: C

    def __init__(self, configuration: C, *args, **kwargs):
        self.configuration = configuration

    def __str__(self) -> str:
        return self.configuration.__str__()

    def __lt__(self, other) -> bool:
        if isinstance(other, DelegatingState):
            return self.configuration.__lt__(other.configuration)
        return self.configuration.__lt__(other)

    def __le__(self, other) -> bool:
        if isinstance(other, DelegatingState):
            return self.configuration.__le__(other.configuration)
        return self.configuration.__le__(other)

    def __eq__(self, other) -> bool:
        if isinstance(other, DelegatingState):
            return self.configuration.__eq__(other.configuration)
        return self.configuration.__eq__(other)

    def __ne__(self, other) -> bool:
        if isinstance(other, DelegatingState):
            return self.configuration.__ne__(other.configuration)
        return self.configuration.__ne__(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, DelegatingState):
            return self.configuration.__gt__(other.configuration)
        return self.configuration.__gt__(other)

    def __ge__(self, other) -> bool:
        if isinstance(other, DelegatingState):
            return self.configuration.__ge__(other.configuration)
        return self.configuration.__ge__(other)

    def __getitem__(self, key):
        if hasattr(self.configuration, "__getitem__") and callable(getattr(self.configuration, "__getitem__")):
            return self.configuration.__getitem__(key)
        if hasattr(self.configuration, key):
            return getattr(self.configuration, key)
        return None


class StringState(DelegatingState[S, str]):
    marked: int

    def __init__(self, configuration: str, marked: int = None, *args, **kwargs):
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


IntPair = TypeVar('IntPair', int, tuple)


class CharGrid(StringState[S]):
    _rows: int
    _cols: int

    def __init__(self, configuration: str, rows: int = 0, cols: int = 0, marked: int = None, *args, **kwargs):
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
        if isinstance(key, tuple) and len(key) == 2:
            key: tuple
            return self.get(*key)
        return super().__getitem__(key)

    def __str__(self) -> str:
        string: str = ""
        for i in range(self._rows):
            string += self.get_row(i) + '\n'
        return string

    def coord(self, i: int) -> tuple:
        if i > self._rows * self._cols: raise IndexError(i)
        return i // self._cols, i % self._cols

    def _flat(self, i: int, j: int) -> int:
        if i == self._rows+1 and j == 0: return self._rows*self._cols
        if i > self._rows or j > self._cols: raise IndexError(i, j)
        return i * self._cols + j

    def get(self, i: IntPair, j: int = None) -> str:
        if isinstance(i, tuple):
            return self.configuration[self._flat(*i)]
        if j is None:
            return self.configuration[i]
        return self.configuration[self._flat(i, j)]

    def get_row(self, i: int) -> str:
        return self.configuration[self._flat(i, 0):self._flat(i + 1, 0)]

    def get_col(self, j: int) -> str:
        string: str = ""
        for i in range(self._rows):
            string += self.configuration[self._flat(i, j)]
        return string

    def swap(self, i: IntPair, j: IntPair = None) -> str:
        if j is not None and isinstance(j, tuple):
            j: tuple
            j: int = self._flat(*j)
        if isinstance(i, tuple):
            i: tuple
            if j is None:
                return super().swap(*i)
            return super().swap(self._flat(*i), j)
        return super().swap(i, j)


class Edge(AEdge[D]):
    cost: N
    source: D
    result: D

    def __init__(self, cost: N = 1, source: D = None, result: D = None, reversible: bool = False, *args, **kwargs):
        self.cost = cost

        self.source = source
        self.result = result
        self.reversible = reversible

    def __str__(self) -> str:
        string: str = ""
        if self.source: string += " " + self.source.name()  ## Clean this name stuff up
        if self.reversible: string += f" <-{self.cost}->"
        else: string += f" -{self.cost}->"
        if self.result: string += " " + self.result.name()

        return string

    def __int__(self) -> int:
        if isinstance(self.cost, int): return self.cost
        return int(self.cost)

    def __float__(self) -> float:
        if isinstance(self.cost, float): return self.cost
        return float(self.cost)

    def __lt__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost < int(other)
        return self.cost < float(other)

    def __le__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost <= int(other)
        return self.cost <= float(other)

    def __eq__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost == int(other)
        return self.cost == float(other)

    def __ne__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost != int(other)
        return self.cost != float(other)

    def __gt__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost > int(other)
        return self.cost > float(other)

    def __ge__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost >= int(other)
        return self.cost >= float(other)


class Action(Edge[D], AAction['Action', S]):
    name: str
    transform: Callable  # further hints

    def __init__(self, name: str, cost: N = 1, transform: Callable = None, source: D = None, result: D = None,
                 reversible: bool = False, *args, **kwargs):
        super().__init__(cost=cost, source=source, result=result)
        self.name = name

        # if result and transform: raise AttributeError(transform, result)

        self.transform = transform

    def __str__(self) -> str:
        string: str = self.name

        if self.source or self.cost != 1 or self.result: string += ":"

        if self.transform: string += " ." + str(self.transform) + "()"
        if self.source: string += " " + self.source.name()  ## Clean this name stuff up
        if self.cost != 1:
            if self.reversible: string += f" <-{self.cost}->"
            else: string += f" -{self.cost}->"
        else:
            if self.reversible: string += f" <--->"
            else: string += f" --->"
        if self.result: string += " " + self.result.name()

        return string


class CostNode(ANode[D], metaclass=ABCMeta):
    cost: N
    _edges: set
    _children: set
    _expanded: bool
    _examined: bool

    def __init__(self, parent: D = None, edge: Action[S, D] = None, cost: N = 0):
        super().__init__(parent)

        self.action = edge
        self.cost = cost

        self._edges = set()
        self._children = set()

        self._expanded = False
        self._examined = False

    def __int__(self) -> int:
        if isinstance(self.cost, int): return self.cost
        return int(self.cost)

    def __float__(self) -> float:
        if isinstance(self.cost, float): return self.cost
        return float(self.cost)

    def __lt__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost < int(other)
        return self.cost < float(other)

    def __le__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost <= int(other)
        return self.cost <= float(other)

    def __eq__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost == int(other)
        return self.cost == float(other)

    def __ne__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost != int(other)
        return self.cost != float(other)

    def __gt__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost > int(other)
        return self.cost > float(other)

    def __ge__(self, other) -> bool:
        if isinstance(self.cost, int):
            return self.cost >= int(other)
        return self.cost >= float(other)

    def __getitem__(self, key: Action[S, D]):
        if isinstance(key, Action): return self.transition(key)
        return None


class StateNode(CostNode[D], Generic[S, D], metaclass=ABCMeta):
    action: Action[S, D]
    state: S
    _transitions: dict  # Further type hints?

    def __init__(self, state: S, parent: D = None, edge: Action[S, D] = None, cost: N = 0,
                 transitions: dict = None, *args, **kwargs):
        super().__init__(parent, edge, cost)

        self.state = state

        self._transitions = transitions

    def expand(self, ignore: Iterable = None) -> set:
        if not self._expanded:
            if ignore:
                self._children = {x for x in self._generate_children() if x not in ignore}
            else:
                self._children = self._generate_children()
            self._expanded = True
        return self._children

    def actions(self) -> set:
        if not self._examined:
            self._actions = self._generate_actions()
            self._examined = True
        return self._actions

    # May need to override

    def __getitem__(self, key: Any):
        if isinstance(key, Action): return super().__getitem__(key)
        return self.state.__getitem__(key)

    def __str__(self) -> str:
        return self.state.__str__()

    def _generate_children(self) -> set:
        return {self.transition(x) for x in self.actions()}

    def name(self) -> str:
        return self.state.__str__()

    def transition(self, action: Action[S, D]) -> D:
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