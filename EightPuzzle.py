from typing import Any

from framework import *

K = TypeVar('K', int, str)

class Puzzle(StateNode['Puzzle', CharGrid]):
    shifts = ["up", "down", "right", "left"]
    _shift_fns = {"up":Puzzle.shift_up, "down":Puzzle.shift_down, "right":Puzzle.shift_right, "left":Puzzle.shift_left}
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    gap: tuple
    _cols: int
    _rows: int
    _is_goal: bool
    _checked_goal: bool

    _gap_char = '0'
    _goal = "123456780"

    state: CharGrid
    parent: "Puzzle"

    def __init__(self, tiles: str = None, parent: "Puzzle" = None, cost: N = 0, edge: Action = None, rows=3, cols=3):
        marked = None
        if not tiles:
            marked = 0
            string = '0'
            for i in range(1, rows * cols):
                if i < 10:
                    string += str(i)
                elif i < 36:
                    string += chr(ord('a') + (i - 10))
                else:
                    raise NotImplementedError(rows, cols)
            tiles = string
        else:
            for i in range(len(tiles)):
                if tiles[i] is Puzzle._gap_char:
                    marked = i
                    break

        if marked is None: raise AttributeError("Missing blank tile", tiles)

        super().__init__(CharGrid(tiles, rows, cols, marked), parent, edge, cost)

        self._rows = rows
        self._cols = cols

        self._is_goal = False
        self._checked_goal = False

        self.gap = self.state.coord(self.state.marked)

    def __getitem__(self, key: Any):
        if isinstance(key, int):
            key: int
            return self.state.get_row(key)
        if isinstance(key, tuple):
            key: tuple
            if len(key) == 2:
                return self.state.get(*key)
        return super().__getitem__(key)

    def name(self) -> str:
        if self.cost > 0:
            return f"Gap at {self.gap} cost: {self.cost}"
        return f"Gap at {self.gap}"

    def can_shift(self, key:K):
        if isinstance(key, int):
            index = key
        elif isinstance(key, str):
            index = Puzzle.shifts.index(key.lower())

        #type = Puzzle.shifts[index]

        if index == 0: # up
            return self.gap[0] < self._rows
        if index == 1: # down
            return self.gap[0] > 0
        if index == 2: # right
            return self.gap[1] < self._cols
        if index == 3: # left
            return self.gap[1] > 0

    def can_shift_up(self):
        return self.can_shift(0)

    def can_shift_down(self):
        return self.can_shift(1)

    def can_shift_right(self):
        return self.can_shift(2)

    def can_shift_left(self):
        return self.can_shift(3)

    def shift(self, key:K, action: Action = None):
        if isinstance(key, int):
            index = key
        elif isinstance(key, str):
            index = Puzzle.shifts.index(key.lower())

        if not self.can_shift(key): return None
        return Puzzle(self.state.swap((self.gap[0] + Puzzle.deltas[index][0], self.gap[1]+ Puzzle.deltas[index][1])), self, self.cost + action.cost, action,
                      self._rows, self._cols)

    def shift_up(self, action: Action = None):
        return self.shift(0, action)

    def shift_down(self, action: Action = None):
        return self.shift(1, action)

    def shift_right(self, action: Action = None):
        return self.shift(2, action)

    def shift_left(self, action: Action = None):
        return self.shift(3, action)

    def _generate_actions(self) -> set:
        action_set = set()

        for shift in Puzzle.shifts:
            if self.can_shift(shift):
                action_set.add(Action(shift, transform=Puzzle._shift_fns[]))

        if self.can_shift_up():
            action_set.add(Action("up", transform=Puzzle.shift_up, source=self))
        if self.can_shift_down():
            action_set.add(Action("down", transform=Puzzle.shift_down, source=self))
        if self.can_shift_left():
            action_set.add(Action("left", transform=Puzzle.shift_up, source=self))
        if self.can_shift_right():
            action_set.add(Action("right", transform=Puzzle.shift_down, source=self))

        return action_set

    def _check_goal(self) -> bool:
        self._checked_goal = True
        self._is_goal = (self.state == Puzzle._goal)
        return self._is_goal

    def is_goal(self) -> bool:
        if self._checked_goal:
            return self._is_goal
        else:
            return self._check_goal()
