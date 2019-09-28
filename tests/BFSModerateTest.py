import unittest

from PuzzleNode import PuzzleNode
from Searcher import Searcher


class SimpleSearchTestCase(unittest.TestCase):
    tiles: str = "136742580"
    gap: tuple = (2, 2)
    puzzle: PuzzleNode = PuzzleNode(tiles)

    output: bool = False

    def test_bfs(self):
        #self.puzzle.debug = True

        searcher: Searcher[PuzzleNode] = Searcher[PuzzleNode]("BFS", self.puzzle, True)  # limit=4, override=True

        if self.output:
            searcher.trace = True
            # searcher.trace_functions = True
            searcher.show_states = True
            searcher.track_expansion = True

        result: PuzzleNode = searcher.search()

        self.assertTrue(result.state.is_goal(), "Final state not goal.")

        self.assertEqual((2, 2), result.state.gap, "")

        self.assertEqual("123456780", result.state.configuration)

        self.assertEqual(10, result.cost)


if __name__ == '__main__':
    unittest.main()
