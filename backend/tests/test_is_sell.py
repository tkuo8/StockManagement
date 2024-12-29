import unittest
from app.service import is_sell


class TestIsBuyFunction(unittest.TestCase):

    def test_buy_signal(self):
        # すべての条件がTrueの場合
        self.assertTrue(is_sell(120, 100, 120, 115))

    def test_short_ma_yesterday_below_short_ma(self):
        # 1番目の条件がFalse: short_ma_yesterday > short_ma
        self.assertFalse(is_sell(120, 100, 110, 105))

    def test_open_below_close(self):
        # 2番目の条件がFalse: open <= close
        self.assertFalse(is_sell(100, 120, 105, 110))

    def test_short_ma_below_close(self):
        # 3番目の条件がFalse: short_ma <= close
        self.assertFalse(is_sell(120, 100, 110, 90))

    def test_short_ma_ge_open_condition(self):
        # 4番目の条件がFalse: (short_ma < open) and ((short_ma - close) / (open - close) < 0.5)
        self.assertFalse(is_sell(120, 100, 110, 105))

    def test_edge_case(self):
        # すべての条件がギリギリでTrueの場合
        self.assertTrue(is_sell(120, 100, 110, 110))


if __name__ == "__main__":
    unittest.main()
