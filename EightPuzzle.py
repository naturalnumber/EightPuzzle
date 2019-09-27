from framework import *

# Type hint used below
K = TypeVar('K', int, str)


class Puzzle(StateNode['Puzzle', CharGrid]):
    # Type hints
    shifts: list
    shift_fns: dict
    deltas: dict
    state: CharGrid
    parent: 'Puzzle'

    # Valid transformations
    shifts = ("up", "down", "right", "left")
    deltas = {"up":(-1, 0), "down":(1, 0), "right":(0, 1), "left":(0, -1)}

    # Instance variables
    gap: tuple
    _cols: int
    _rows: int
    _is_goal: bool
    _checked_goal: bool

    _gap_char = '0'
    _goal = "123456780"
    _action_cost: int

    debug = False

    def __init__(self, tiles: str = None, parent: 'Puzzle' = None, cost: N = 0, edge: Action[CharGrid, 'Puzzle'] = None,
                 rows=3, cols=3):
        """
        This method initialized a Puzzle node.
        :param tiles: The tile values, will generate if empty
        :param parent: The optional parent of this node
        :param cost: The cumulative cost to reach this node, defaults to 0
        :param edge: The optional action connecting this node to the parent
        :param rows: The number of rows, defaults to 3
        :param cols: The number of columns, defaults to 3
        """

        # The shift function references
        self.shift_fns = {"up":self.shift_up, "down":self.shift_down, "right":self.shift_right, "left":self.shift_left}

        # Finds and marks the 0, or generates a tile set if none were provided
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

        # Sending details to the super class and creation of the state
        super().__init__(CharGrid(tiles, rows, cols, marked), parent, edge, cost)

        # Instance variables
        self._rows = rows
        self._cols = cols

        self._bad_tiles = 0
        self._disorder = 0
        self._is_goal = False
        self._checked_goal = False

        self.gap = self.state.coord(self.state.marked)

        self.action_cost = 1

        self.state.debug = self.debug

        self._name = None

        # Checks to see if the state is a goal
        self.is_goal()

    # Helper method
    def describe(self) -> str:
        """
        :return: A string description of the node
        """
        if self._name is None:
            self._name = self._gap_char+f" at {self.gap}"
            if self._checked_goal:
                if self.is_goal():
                    self._name += " Goal!"
                self._name += f" with {self._bad_tiles} tiles off by {self._disorder} total"
            if self.cost > 0:
                self._name += f" after {self.cost} steps"
        return self._name

    # Checks possibility of shift
    def can_shift(self, key: K) -> bool:
        """
        :param key: The shift to check
        :return: Whether or not the shift is possible
        """
        if isinstance(key, int):
            shift_type = Puzzle.shifts[key]
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

    def shift(self, key: K, action: Action = None, *args, **kwargs) -> 'Puzzle':
        """
        Performs a given transformation
        :param key: The shift to perform
        :param action: The optional associated action
        :return:
        """
        # Debug output
        if self.debug: print(f"Puzzle.shift({key}, {action}")

        # Decipher keu
        shift_type: str
        if isinstance(key, int):
            shift_type = Puzzle.shifts[key]
        else:
            shift_type = str(key)

        # Calculate cost
        if action:
            d_cost = action.cost
        else:
            d_cost = self.action_cost

        # Debug output
        if self.debug: print(f"\ttype={shift_type}, cost={d_cost}, can={self.can_shift(shift_type)}")

        # Determine result
        if not self.can_shift(shift_type): result = None
        else: result = Puzzle(self.state.swap((self.gap[0] + Puzzle.deltas[shift_type][0],
                                               self.gap[1] + Puzzle.deltas[shift_type][1])),
                              self, self.cost + d_cost, action, self._rows, self._cols)

        # Update action
        if action and not action.result: action.result = result

        return result

    # For function linking
    def shift_up(self, action: Action = None, *args, **kwargs) -> 'Puzzle':
        return self.shift("up", action, *args, **kwargs)

    def shift_down(self, action: Action = None, *args, **kwargs) -> 'Puzzle':
        return self.shift("down", action, *args, **kwargs)

    def shift_right(self, action: Action = None, *args, **kwargs) -> 'Puzzle':
        return self.shift("right", action, *args, **kwargs)

    def shift_left(self, action: Action = None, *args, **kwargs) -> 'Puzzle':
        return self.shift("left", action, *args, **kwargs)

    def _generate_actions(self) -> list:
        """
        Internal method for generating a list of valid actions.
        :return: A list of valid actions
        """
        # Debug output
        if self.debug: print(f"StateNode._generate_actions()")
        action_set = []

        # Check every shift
        for shift in Puzzle.shifts:
            if self.can_shift(shift):
                action_set.append(Action(shift, transform=self.shift_fns[shift], source=self))

        return action_set

    def _check_goal(self) -> bool:
        """
        Internal method for goal checking
        :return: The goal status
        """
        self._checked_goal = True
        self._is_goal = (self.state == Puzzle._goal)
        for i in range(len(self.state.configuration)):
            if self.state.configuration[i] != Puzzle._goal[i]:
                self._bad_tiles += 1  # Heuristic calculation
                n = int(self.state.configuration[i])
                l = i+1 % self._rows * self._cols
                self._disorder += abs((l // self._cols) - (n // self._cols)) + abs(
                    (l % self._cols) - (n % self._cols))  # Heuristic calculation

        return self._is_goal

    def is_goal(self) -> bool:
        """
        :return: Whether or not this node contains a goal
        """
        if self._checked_goal:
            return self._is_goal
        else:
            return self._check_goal()

    # Override operator
    def __getitem__(self, key: Any):
        if isinstance(key, int):
            key: int
            return self.state.get_row(key)
        if isinstance(key, tuple):
            key: tuple
            if len(key) == 2:
                return self.state.get(*key)
        return super().__getitem__(key)
