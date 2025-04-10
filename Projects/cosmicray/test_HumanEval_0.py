
import unittest
from HumanEval_0 import has_close_elements

class Test_Has_close_elements(unittest.TestCase):
    METADATA = {
    'author': 'jt',
    'dataset': 'test'
}

    def test_has_close_elements(self):
        self.check(has_close_elements)

    def check(self, has_close_elements):
        assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
        assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
        assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
        assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
        assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
        assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
        assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False

if __name__ == "__main__":
    unittest.main()
