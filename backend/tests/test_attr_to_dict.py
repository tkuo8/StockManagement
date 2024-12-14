import unittest
from app.util import attr_to_dict

class TestAttrToDict(unittest.TestCase):
    def setUp(self):
        # テスト用クラス
        class TestClass:
            def __init__(self):
                self.public_attr = 42
                self._private_attr = "hidden"
                self.__magic_attr__ = "magic"
                self.method = lambda: "I'm callable"
        
        self.test_obj = TestClass()

    def test_attr_to_dict(self):
        # attr_to_dictの出力
        result = attr_to_dict(self.test_obj)
        
        # 期待される辞書
        expected = {
            "public_attr": 42,
            "_private_attr": "hidden",
        }
        
        # アサーション
        self.assertEqual(result, expected)

    def test_empty_object(self):
        class EmptyClass:
            pass

        empty_obj = EmptyClass()
        result = attr_to_dict(empty_obj)
        self.assertEqual(result, {})  # 空のオブジェクトは空の辞書を返す

if __name__ == "__main__":
    unittest.main()
