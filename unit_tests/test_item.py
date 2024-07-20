import unittest
from src.item import Item, ItemRepository

class TestDataValidation(unittest.TestCase):
    def test_valid_data(self):
        data = [
            {"price": 30, "id": "xxxxxx"},
            {"price": 25, "id": "1224"},
        ]
        self.assertEqual(data,Item("50g Handler","A 50 g item for handling",500))
        self.assertEqual(1,4)

if __name__ == '__main__':
    unittest.main()
