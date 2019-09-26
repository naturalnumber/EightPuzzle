from Framework import *


class Puzzle(StateNode):
    gap: tuple[int, int]
    _cols: int
    _rows: int
    _is_goal: bool
    _checked_goal: bool

    _gap_char = '0'
    _goal = "123456780"

    state: CharGrid
    parent: StateNode

    def __init__(self, tiles: str = "", parent: Puzzle = False, cost: N = 0, action: Action = False, rows=3,
                 cols=3):
        marked = 0
        if not tiles:
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

        super().__init__(CharGrid(tiles, rows, cols, marked), parent, action, cost)

        self._rows = rows
        self._cols = cols

        self._is_goal = False
        self._checked_goal = False

        self.gap = self.state.coord(self.state.marked)

    def __getitem__(self, key):
        if type(key) is int:
            key: int
            return self.state.get_row(key)
        if type(key) is tuple:
            key: tuple
            if len(key) == 2:
                return self.state.get(*key)
        return super().__getitem__(key)

    def name(self) -> str:
        return f"Gap at {self.gap}"

    def shift_up(self, action: Action = None):
        return Puzzle(self.state.swap((self.gap[0] + 1, self.gap[1])), self, self.cost + 1, action,
                      self._rows, self._cols)

    def shift_down(self, action: Action = None):
        return Puzzle(self.state.swap((self.gap[0] - 1, self.gap[1])), self, self.cost + 1, action,
                      self._rows, self._cols)

    def shift_left(self, action: Action = None):
        return Puzzle(self.state.swap((self.gap[0] + 1, self.gap[1] + 1)), self, self.cost + 1, action,
                      self._rows, self._cols)

    def shift_right(self, action: Action = None):
        return Puzzle(self.state.swap((self.gap[0], self.gap[1] - 1)), self, self.cost + 1, action,
                      self._rows, self._cols)

    def _generate_actions(self) -> set:
        action_set = set()

        if self.gap[0] < self._rows:
            action_set.add(Action("up", transform=Puzzle.shift_up, target=self))
        if self.gap[0] > 0:
            action_set.add(Action("down", transform=Puzzle.shift_down, target=self))
        if self.gap[1] < self._cols:
            action_set.add(Action("left", transform=Puzzle.shift_up, target=self))
        if self.gap[1] > 0:
            action_set.add(Action("right", transform=Puzzle.shift_down, target=self))

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
