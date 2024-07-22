import unittest
from src.item import Item, ItemRepository


class TestItemRepository(unittest.TestCase):
    def setUp(self):
        self.item_repo = ItemRepository()

    @unittest.skip("Skipping test_get_items for demonstration purposes")
    def test_create_item(self):
        item = self.item_repo.create_item(
            "Ergonomic Keyboard", "Comfortable keyboard for long typing sessions", 79.99
        )
        self.assertIsInstance(item, Item)
        self.assertEqual(item.name, "Ergonomic Keyboard")
        self.assertEqual(
            item.description, "Comfortable keyboard for long typing sessions"
        )
        self.assertEqual(item.price, 79.99)

    def test_get_item(self):
        item = self.item_repo.create_item(
            "Ergonomic Mouse V2", "Elegant mouse for professional work", 49.99
        )
        retrieved_item = self.item_repo.get_item(item.sku)
        self.assertIsInstance(retrieved_item, Item)
        self.assertEqual(retrieved_item.name, "Ergonomic Mouse V2")
        self.assertEqual(
            retrieved_item.description, "Elegant mouse for professional work"
        )
        self.assertEqual(retrieved_item.price, 49.99)

    def test_get_item_nonexistent(self):
        self.assertIsNone(self.item_repo.get_item("nonexistent_sku"))

    @unittest.skip("Method Not Implemented")
    def test_get_items(self):
        items = self.item_repo.get_items()
        self.assertIsInstance(items, list)
        self.assertGreaterEqual(len(items), 0)
        for item in items:
            self.assertIsInstance(item, Item)

    @unittest.skip("Skipping test_get_items for demonstration purposes")
    def test_update_item(self):
        item = self.item_repo.create_item(
            "Ergonomic Monitor", "High-quality monitor for professional work", 199.99
        )
        updated_item = self.item_repo.update_item(
            item.sku,
            "Ergonomic Monitor",
            "High-quality monitor for professional work",
            249.99,
        )
        self.assertIsInstance(updated_item, Item)
        self.assertEqual(updated_item.name, "Ergonomic Monitor")
        self.assertEqual(
            updated_item.description, "High-quality monitor for professional work"
        )
        self.assertEqual(updated_item.price, 249.99)

    @unittest.skip("Skipping test_get_items for demonstration purposes")
    def test_delete_item(self):
        item = self.item_repo.create_item(
            "Ergonomic Headphones",
            "Noise-cancelling headphones for immersive audio experience",
            99.99,
        )
        deleted_item = self.item_repo.delete_item(item.sku)
