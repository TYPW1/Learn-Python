import unittest
from calculator import mul

class CalculatorTest(unittest.TestCase):
    def test_mul_positive_numbers(self):
        self.assertEqual(mul(2, 3), 6)

    def test_mul_negative_numbers(self):
        self.assertEqual(mul(-2, -3), 6)

    def test_mul_positive_and_negative(self):
        self.assertEqual(mul(2, -3), -6)

    def test_mul_with_one_zero(self):
        self.assertEqual(mul(2, 0), 0)  # Only one zero case tested (y = 0)

if __name__ == "__main__":
    unittest.main()
