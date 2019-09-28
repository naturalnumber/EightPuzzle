from EightPuzzle import EightPuzzle
from framework import *

# Type hint used below
K = TypeVar('K', int, str)

Tiles = TypeVar('Tiles', EightPuzzle, str)


class PuzzleNode(StateNode['PuzzleNode', EightPuzzle]):
    # Type hints
    state: EightPuzzle
    parent: 'PuzzleNode'

    # Instance variables
    _cols: int
    _rows: int

    _action_cost: int

    debug = False

    def __init__(self, tiles: Tiles = None, parent: 'PuzzleNode' = None, cost: N = 0,
                 edge: Action[EightPuzzle, 'PuzzleNode'] = None,
                 rows: int = 3, cols: int = 3):
        """
        This method initializes a PuzzleNode node.
        :param tiles: The tile values, will generate if empty
        :param parent: The optional parent of this node
        :param cost: The cumulative cost to reach this node, defaults to 0
        :param edge: The optional action connecting this node to the parent
        :param rows: The number of rows, defaults to 3
        :param cols: The number of columns, defaults to 3
        """
        # The shift function references
        self.shift_fns = {"up":self.shift_up, "down":self.shift_down, "right":self.shift_right, "left":self.shift_left}

        # Ggenerates a tile set if none were provided
        if not tiles:
            tiles = EightPuzzle.generate_tiles(rows, cols)

        # Sending details to the super class and creation of the state
        if isinstance(tiles, EightPuzzle):
            super().__init__(tiles, parent, edge, cost)
        else:
            super().__init__(EightPuzzle(tiles, rows, cols), parent, edge, cost)

        # Instance variables
        self._rows = rows
        self._cols = cols

        self.action_cost = 1

        self.state.debug = self.debug

        self._name = None
        self._description = None

    # Helper method
    def describe(self) -> str:
        """
        :return: A string description of the node
        """
        if self._description is None:
            self._description = ""
            if self._name: self._description += self._name + " "
            if not self.parent: self._description += "head node "
            self._description += self.state.describe()
            if self.cost > 0:
                self._description += f" after {self.cost} steps"
        return self._description

    def shift(self, key: K, action: Action = None, *args, **kwargs) -> 'PuzzleNode':
        """
        Performs a given transformation
        :param key: The shift to perform
        :param action: The optional associated action
        :return:
        """
        # Debug output
        if self.debug: print(f"PuzzleNode.shift({key}, {action}")

        # Calculate cost
        if action:
            d_cost = action.cost
        else:
            d_cost = self.action_cost

        # Determine result
        if not self.state.can_shift(key): result = None
        else: result = PuzzleNode(self.state.shift(key, action, args, kwargs),
                                  self, self.cost + d_cost, action, self._rows, self._cols)

        # Update action
        if action and not action.result: action.result = result

        return result

    # For function linking
    def shift_up(self, action: Action = None, *args, **kwargs) -> 'PuzzleNode':
        return self.shift("up", action, *args, **kwargs)

    def shift_down(self, action: Action = None, *args, **kwargs) -> 'PuzzleNode':
        return self.shift("down", action, *args, **kwargs)

    def shift_right(self, action: Action = None, *args, **kwargs) -> 'PuzzleNode':
        return self.shift("right", action, *args, **kwargs)

    def shift_left(self, action: Action = None, *args, **kwargs) -> 'PuzzleNode':
        return self.shift("left", action, *args, **kwargs)

    def _generate_actions(self) -> list:
        """
        Internal method for generating a list of valid actions.
        :return: A list of valid actions
        """
        # Debug output
        if self.debug: print(f"PuzzleNode._generate_actions()")
        action_set = []

        # Check every shift
        for shift in self.state.shifts:
            if self.state.can_shift(shift):
                action_set.append(Action(shift, transform=self.shift_fns[shift], source=self))

        return action_set

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
