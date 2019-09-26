import unittest

from Framework import *


# noinspection DuplicatedCode
class ActionTest(unittest.TestCase):
    def test_action(self):
        action = Action("Test Action", 0.5)
        self.assertEqual(action.name, "Test Action")
        self.assertEqual(action.cost, 0.5)

    def test_compare_eq(self):
        action5a = Action("Test Action 0.5a", 0.5)
        action5b = Action("Test Action 0.5b", 0.5)

        self.assertEqual(action5a == action5b, True)
        self.assertEqual(action5a != action5b, False)
        self.assertEqual(action5a < action5b, False)
        self.assertEqual(action5a <= action5b, True)
        self.assertEqual(action5a >= action5b, True)
        self.assertEqual(action5a > action5b, False)

    def test_compare_eq_2(self):
        action2i = Action("Test Action 2", 2)
        action2f = Action("Test Action 2.0", 2.0)

        self.assertEqual(action2i == action2f, True)
        self.assertEqual(action2i != action2f, False)
        self.assertEqual(action2i < action2f, False)
        self.assertEqual(action2i <= action2f, True)
        self.assertEqual(action2i >= action2f, True)
        self.assertEqual(action2i > action2f, False)

    def test_compare_lt(self):
        action5 = Action("Test Action 5", 5)
        action1 = Action("Test Action 1", 1)

        self.assertEqual(action1 == action5, False)
        self.assertEqual(action1 != action5, True)
        self.assertEqual(action1 < action5, True)
        self.assertEqual(action1 <= action5, True)
        self.assertEqual(action1 >= action5, False)
        self.assertEqual(action1 > action5, False)

    def test_compare_gt(self):
        action5 = Action("Test Action 5", 5)
        action1 = Action("Test Action 1", 1)

        self.assertEqual(action5 == action1, False)
        self.assertEqual(action5 != action1, True)
        self.assertEqual(action5 < action1, False)
        self.assertEqual(action5 <= action1, False)
        self.assertEqual(action5 >= action1, True)
        self.assertEqual(action5 > action1, True)

    def test_cast(self):
        action5 = Action("Test Action 0.5", 0.5)
        action1 = Action("Test Action 1", 1)

        self.assertEqual(float(action5), 0.5)
        self.assertEqual(int(action1), 1)


if __name__ == '__main__':
    unittest.main()
