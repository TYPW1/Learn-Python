import unittest
from simple import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        print("Running test_add...")

        # Test correct results
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-2, -3), -5)
        self.assertEqual(self.calc.add(0, 5), 5)
        self.assertEqual(self.calc.add(1000, 2000), 3000)

        # Ensure specific incorrect results are caught for mutants
        self.assertNotEqual(self.calc.add(2, 3), 6)  # Catch + -> *
        self.assertNotEqual(self.calc.add(2, 3), -1)  # Catch + -> -
        self.assertNotEqual(self.calc.add(2, 3), 8)  # Catch + -> **

        # Add additional cases to catch multiplication mutant
        self.assertNotEqual(self.calc.add(1, 0), 0)  # Catch + -> *
        self.assertNotEqual(self.calc.add(3, 3), 9)  # Catch + -> *
        self.assertNotEqual(self.calc.add(-2, 2), -4)  # Catch + -> *

        # Add additional edge cases
        self.assertEqual(self.calc.add(0, 0), 0)  # Ensure no-op works
        self.assertEqual(self.calc.add(-1, 1), 0)  # Negative + positive


if __name__ == "__main__":
    unittest.main(verbosity=2)
