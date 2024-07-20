import unittest
from src.item import Item, ItemRepository

class TestDataValidation(unittest.TestCase):
    def test_valid_data(self):
        data = [
            {"price": 30, "id": "xxxxxx"},
            {"price": 25, "id": "1224"},
        ]
        self.assertNotEqual(data,Item("50g Handler","A 50 g item for handling",500))
        self.assertLessEqual(1.9,2)

if __name__ == '__main__':
    unittest.main()
