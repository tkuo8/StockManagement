import unittest
from app.service import is_exclusion


class TestIsBuyFunction(unittest.TestCase):

    def test_exclusion_signal(self):
        # すべての条件がTrueの場合
        self.assertTrue(is_exclusion(100, 120))

    def test_exclusion_signal(self):
        # すべての条件がギリギリでFalseの場合
        self.assertFalse(is_exclusion(120, 120))

    def test_exclusion_signal(self):
        # すべての条件がFalseの場合
        self.assertFalse(is_exclusion(120, 110))


if __name__ == "__main__":
    unittest.main()
