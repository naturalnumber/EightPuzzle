import unittest

from EightPuzzle import Puzzle


class BasicTestCase(unittest.TestCase):
    puzzle: Puzzle = Puzzle("012345678")

    def test_gap(self):
        self.assertEqual((0, 0), self.puzzle.gap)

    def test_name(self):
        self.assertEqual("Gap at (0, 0)", self.puzzle.name())

    def test_index_2d(self):
        for i in range(9):
            self.assertEqual(str(i), self.puzzle[i // 3][i % 3])

    def test_index_pair(self):
        for i in range(9):
            self.assertEqual(str(i), self.puzzle[i // 3, i % 3])

    def test_index_tuple(self):
        for i in range(9):
            self.assertEqual(str(i), self.puzzle[(i // 3,i % 3)])

    def test_get_row(self):
        self.assertEqual("012", self.puzzle[0])
        self.assertEqual("345", self.puzzle[1])
        self.assertEqual("678", self.puzzle[2])

    def test_index_error(self):
        with self.assertRaises(IndexError):
            print(self.puzzle[4])
        with self.assertRaises(IndexError):
            print(self.puzzle[3, 0])
        with self.assertRaises(IndexError):
            print(self.puzzle[(3, 0)])

    def test_up(self):
        new = self.puzzle.shift_up()


if __name__ == '__main__':
    unittest.main()
