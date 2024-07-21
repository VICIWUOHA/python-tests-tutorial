import unittest
from src.item import Item, ItemRepository





class TestDataValidation(unittest.TestCase):

    def setUp(self):
        self.item_repo = ItemRepository()
        # return item_repo

    def test_create_item(self, ):
        item = Item("item1", "This is a test item", 10.0)
        self.assertEqual(item.name, "item1")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.price, 10.0)

    def test_item_repository(self):
        self.item_repo.create_item("item2", "Another test item", 15.0)
        self.assertEqual(len(repo.items), 1)
        self.assertEqual(repo.items[0].name, "item2")
        self.assertEqual(repo.items[0].description, "Another test item")
        self.assertEqual(repo.items[0].price, 15.0)

    def test_item_validation(self):
        with self.assertRaises(ValueError):
            Item("", "Invalid name", 10.0)
        with self.assertRaises(ValueError):
            Item("item3", "Valid name", -5.0)

       

if __name__ == '__main__':
    unittest.main()
