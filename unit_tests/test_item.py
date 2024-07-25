import unittest
from src.item import Item
# , ItemRepository


class TestItem(unittest.TestCase):
    def test_item_validation(self):
        with self.assertRaises(ValueError):
            Item("External SSD", "High-speed storage for data transfer", -5.0)


if __name__ == "__main__":
    unittest.main()
