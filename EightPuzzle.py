from typing import TypeVar

from framework import CharGrid, Action

# Type hint used below
K = TypeVar('K', int, str)


class EightPuzzle(CharGrid):
    # Constants
    _gap_char = '0'
    _goal = "123456780"
    shifts: list
    shift_fns: dict
    deltas: dict
    shifts = ("up", "down", "right", "left")
    deltas = {"up":(-1, 0), "down":(1, 0), "right":(0, 1), "left":(0, -1)}
    reverses = {"up":"down", "down":"up", "right":"left", "left":"right"}

    # Instance variables
    _is_goal: bool
    _checked_goal: bool

    def __init__(self, tiles: str, rows: int = 3, cols: int = 3):
        """
        This method initializes an EightPuzzle grid.
        :param tiles: The tile values
        :param rows: The number of rows, defaults to 3
        :param cols: The number of columns, defaults to 3
        """

        # The shift function references
        self.shift_fns = {"up":self.shift_up, "down":self.shift_down, "right":self.shift_right, "left":self.shift_left}

        # Finds and marks the 0
        marked = None

        for i in range(len(tiles)):
            if tiles[i] is self._gap_char:
                marked = i
                break

        if marked is None: raise AttributeError("Missing blank tile", tiles)

        # Sending details to the super class and creation of the state
        super().__init__(tiles, rows, cols, marked)

        # Instance variables
        self._bad_tiles = 0
        self._disorder = 0
        self._is_goal = False
        self._checked_goal = False

        self._name = None
        self._description = None

        # Checks to see if the state is a goal
        self.is_goal()

    # Helper method
    def describe(self) -> str:
        """
        :return: A string description of the node
        """
        if self._description is None:
            self._description = ""
            if self._name: self._description += self._name + " "
            self._description += self._gap_char + f" at {self.gap}"
            if self._checked_goal:
                if self.is_goal():
                    self._description += " Goal!"
                else:
                    self._description += f" with {self._bad_tiles} tiles off by {self._disorder} total"
        return self._description

    # Checks possibility of shift
    def can_shift(self, key: K) -> bool:
        """
        :param key: The shift to check
        :return: Whether or not the shift is possible
        """
        if isinstance(key, int):
            shift_type = self.shifts[key]
        else:
            shift_type = key

        if shift_type == "up":
            return self.gap[0] > 0
        if shift_type == "down":
            return self.gap[0] < self._rows - 1
        if shift_type == "right":
            return self.gap[1] < self._cols - 1
        if shift_type == "left":
            return self.gap[1] > 0

    # For function linking
    def can_shift_up(self) -> bool:
        return self.can_shift(0)

    def can_shift_down(self) -> bool:
        return self.can_shift(1)

    def can_shift_right(self) -> bool:
        return self.can_shift(2)

    def can_shift_left(self) -> bool:
        return self.can_shift(3)

    def shift(self, key: K, action: Action = None, *args, **kwargs) -> 'EightPuzzle':
        """
        Performs a given transformation
        :param key: The shift to perform
        :param action: The optional associated action
        :return:
        """
        # Debug output
        if self.debug: print(f"EightPuzzle.shift({key}, {action}")

        # Decipher key
        shift_type: str
        if isinstance(key, int):
            shift_type = EightPuzzle.shifts[key]
        else:
            shift_type = str(key)

        # Debug output
        if self.debug: print(f"\ttype={shift_type}, can={self.can_shift(shift_type)}")

        # Determine result
        if not self.can_shift(shift_type): result = None
        else: result = EightPuzzle(self.swap((self.gap[0] + self.deltas[shift_type][0],
                                              self.gap[1] + self.deltas[shift_type][1])),
                                   self._rows, self._cols)

        # Update action
        if action and not action.result: action.result = result

        return result

    # For function linking
    def shift_up(self, action: Action = None, *args, **kwargs) -> 'EightPuzzle':
        return self.shift("up", action, *args, **kwargs)

    def shift_down(self, action: Action = None, *args, **kwargs) -> 'EightPuzzle':
        return self.shift("down", action, *args, **kwargs)

    def shift_right(self, action: Action = None, *args, **kwargs) -> 'EightPuzzle':
        return self.shift("right", action, *args, **kwargs)

    def shift_left(self, action: Action = None, *args, **kwargs) -> 'EightPuzzle':
        return self.shift("left", action, *args, **kwargs)

    def _check_goal(self) -> bool:
        """
        Internal method for goal checking
        :return: The goal status
        """
        self._checked_goal = True
        self._is_goal = (self.configuration == self._goal)
        for i in range(len(self.configuration)):
            if self.configuration[i] != self._goal[i]:
                self._bad_tiles += 1  # Heuristic calculation
                n = int(self.configuration[i])
                l = i + 1 % self._rows * self._cols
                self._disorder += abs((l // self._cols) - (n // self._cols)) \
                                  + abs((l % self._cols) - (n % self._cols))  # Heuristic calculation
        return self._is_goal

    def is_goal(self) -> bool:
        """
        :return: Whether or not this node contains a goal
        """
        if self._checked_goal:
            return self._is_goal
        else:
            return self._check_goal()

    def _generate_actions(self) -> list:
        """
        Internal method for generating a list of valid actions.
        :return: A list of valid actions
        """
        # Debug output
        if self.debug: print(f"EightPuzzle._generate_actions()")
        action_set = []

        # Check every shift
        for shift in self.shifts:
            if self.can_shift(shift):
                action_set.append(Action(shift, transform=self.shift_fns[shift], argument=self, reversible=True,
                                         reverse=self.reverses[shift]))

        return action_set

    @staticmethod
    def generate_tiles(rows: int, cols: int) -> str:
        # marked = 0
        tiles = '0'
        for i in range(1, rows * cols):
            if i < 10:
                tiles += str(i)
            elif i < 36:
                tiles += chr(ord('a') + (i - 10))
            else:
                raise NotImplementedError(rows, cols)
        return tiles

    @staticmethod
    def is_puzzle(term: str) -> bool:
        if not isinstance(term, str) or len(term) != 9:
            return False
        if len(term.translate({ord(i):None for i in '012345678'})) != 0:
            return False
        for c in '012345678':
            if c not in term:
                return False
        return True
