import unittest

from PuzzleNode import PuzzleNode


class BasicTestCase1(unittest.TestCase):
    tiles: str = "012345678"
    gap: tuple = (0, 0)
    puzzle: PuzzleNode = PuzzleNode(tiles)

    output: bool = False

    def test_gap(self):
        self.assertEqual(self.gap, self.puzzle.state.gap)

    # def test_name(self):
    #    self.assertEqual(f"0 at {self.gap}", self.puzzle.describe()[0:11])

    def test_index_2d(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[i // 3][i % 3])

    def test_index_pair(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[i // 3, i % 3])

    def test_index_tuple(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[(i // 3, i % 3)])

    def test_get_row(self):
        self.assertEqual(self.tiles[0:3], self.puzzle[0])
        self.assertEqual(self.tiles[3:6], self.puzzle[1])
        self.assertEqual(self.tiles[6:9], self.puzzle[2])

    def test_index_error(self):
        with self.assertRaises(IndexError):
            print(self.puzzle[4])
        with self.assertRaises(IndexError):
            print(self.puzzle[3, 0])
        with self.assertRaises(IndexError):
            print(self.puzzle[(3, 0)])

    def test_goal(self):
        self.assertFalse(self.puzzle.state.is_goal())

    def test_actions(self):
        actions = self.puzzle.actions()

        for dir in self.puzzle.state.shifts:
            if self.puzzle.state.can_shift(dir):
                self.assertEqual(1, len([x for x in actions if x.name is dir]))


'''
    def test_up(self):
        dir = "up"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_down(self):
        dir = "down"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_right(self):
        dir = "right"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_left(self):
        dir = "left"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)
'''


class BasicTestCase2(unittest.TestCase):
    tiles: str = "123405678"
    gap: tuple = (1, 1)
    puzzle: PuzzleNode = PuzzleNode(tiles)

    output: bool = False

    def test_gap(self):
        self.assertEqual(self.gap, self.puzzle.state.gap)

    # def test_name(self):
    #    self.assertEqual(f"0 at {self.gap}", self.puzzle.describe()[0:11])

    def test_index_2d(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[i // 3][i % 3])

    def test_index_pair(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[i // 3, i % 3])

    def test_index_tuple(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[(i // 3, i % 3)])

    def test_get_row(self):
        self.assertEqual(self.tiles[0:3], self.puzzle[0])
        self.assertEqual(self.tiles[3:6], self.puzzle[1])
        self.assertEqual(self.tiles[6:9], self.puzzle[2])

    def test_index_error(self):
        with self.assertRaises(IndexError):
            print(self.puzzle[4])
        with self.assertRaises(IndexError):
            print(self.puzzle[3, 0])
        with self.assertRaises(IndexError):
            print(self.puzzle[(3, 0)])

    def test_goal(self):
        self.assertFalse(self.puzzle.state.is_goal())

    def test_actions(self):
        actions = self.puzzle.actions()

        for dir in self.puzzle.state.shifts:
            if self.puzzle.state.can_shift(dir):
                self.assertEqual(1, len([x for x in actions if x.name is dir]))


'''
    def test_up(self):
        dir = "up"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_down(self):
        dir = "down"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_right(self):
        dir = "right"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_left(self):
        dir = "left"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)
'''


class BasicTestCase3(unittest.TestCase):
    tiles: str = "123456780"
    gap: tuple = (2, 2)
    puzzle: PuzzleNode = PuzzleNode(tiles)

    output: bool = False

    def test_gap(self):
        self.assertEqual(self.gap, self.puzzle.state.gap)

    # def test_name(self):
    #    self.assertEqual(f"0 at {self.gap}", self.puzzle.describe()[0:11])

    def test_index_2d(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[i // 3][i % 3])

    def test_index_pair(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[i // 3, i % 3])

    def test_index_tuple(self):
        for i in range(9):
            self.assertEqual(self.tiles[i], self.puzzle[(i // 3, i % 3)])

    def test_get_row(self):
        self.assertEqual(self.tiles[0:3], self.puzzle[0])
        self.assertEqual(self.tiles[3:6], self.puzzle[1])
        self.assertEqual(self.tiles[6:9], self.puzzle[2])

    def test_index_error(self):
        with self.assertRaises(IndexError):
            print(self.puzzle[4])
        with self.assertRaises(IndexError):
            print(self.puzzle[3, 0])
        with self.assertRaises(IndexError):
            print(self.puzzle[(3, 0)])

    def test_goal(self):
        self.assertTrue(self.puzzle.state.is_goal())

    def test_actions(self):
        actions = self.puzzle.actions()

        for dir in self.puzzle.state.shifts:
            if self.puzzle.state.can_shift(dir):
                self.assertEqual(1, len([x for x in actions if x.name is dir]))


'''
    def test_up(self):
        dir = "up"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_down(self):
        dir = "down"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_right(self):
        dir = "right"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)

    def test_left(self):
        dir = "left"
        new = self.puzzle.shift(dir)

        if self.output:
            print(dir)
            print(new)

        if self.puzzle.state.can_shift(dir):
            self.assertEqual((self.gap[0] + self.puzzle.state.deltas[dir][0],
                              self.gap[1] + self.puzzle.state.deltas[dir][1]),
                             new.state.gap)
        else:
            self.assertIsNone(new)
'''

'''
class ModerateSearchTestCase(unittest.TestCase):
    tiles: str = "130426758"
    gap: tuple = (0, 2)
    puzzle: PuzzleNode = PuzzleNode(tiles)

    output: bool = False

    def test_bfs(self):
        #self.puzzle.debug = True

        searcher: Searcher[PuzzleNode] = Searcher[PuzzleNode]("BFS", self.puzzle, True, limit=4, override=True)

        searcher.trace = True
        # searcher.trace_functions = True

        result: PuzzleNode = searcher.search()

        self.assertTrue(result.is_goal(), "Final state not goal.")

        self.assertEqual((2, 2), result.gap, "")

        self.assertEqual("123456780", result.state.configuration)

        self.assertEqual(2, result.cost)
'''

if __name__ == '__main__':
    unittest.main()
