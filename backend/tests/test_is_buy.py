import unittest
from app.service import is_buy


class TestIsBuyFunction(unittest.TestCase):

    def test_buy_signal(self):
        # すべての条件がTrueの場合
        self.assertTrue(is_buy(100, 120, 105, 110, 90))

    def test_very_long_ma_above_close(self):
        # 1番目の条件がFalse: very_long_ma >= close
        self.assertFalse(is_buy(100, 120, 105, 110, 125))

    def test_short_ma_yesterday_above_short_ma(self):
        # 2番目の条件がFalse: short_ma_yesterday > short_ma
        self.assertFalse(is_buy(100, 120, 110, 105, 90))

    def test_open_above_close(self):
        # 3番目の条件がFalse: open >= close
        self.assertFalse(is_buy(130, 120, 105, 110, 90))

    def test_short_ma_above_close(self):
        # 4番目の条件がFalse: short_ma >= close
        self.assertFalse(is_buy(100, 120, 110, 125, 90))

    def test_short_ma_le_open_condition(self):
        # 5番目の条件がFalse: (short_ma > open) and ((close - short_ma) / (close - open) < 0.5)
        self.assertFalse(is_buy(100, 120, 110, 130, 90))

    def test_edge_case(self):
        # すべての条件がギリギリでTrueの場合
        self.assertTrue(is_buy(100, 120, 110, 110, 119))


if __name__ == "__main__":
    unittest.main()
