import unittest
from src.item_repository import ItemRepository
from src.item import Item


class TestItemRepository(unittest.TestCase):
    def setUp(self):
        self.item_repo = ItemRepository()
        # would update to setup items later

    # @unittest.skip("Uncomment to Skip test_create_items for demonstration purposes")
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

    def test_get_all_items(self):
        items = self.item_repo.get_all_items()
        self.assertIsInstance(items, list)
        self.assertGreaterEqual(len(items), 0)
        for item in items:
            self.assertIsInstance(item, Item)

    def test_update_item(self):
        item = self.item_repo.create_item(
            "Ergonomic Monitor", "High-quality monitor for professional work", 199.99
        )
        updated_item = self.item_repo.update_item(
            Item(
                "Ergonomic Monitor",
                "High-quality monitor for professional work and bustle",
                249.99,
                item.sku,
            )
        )
        self.assertIsInstance(updated_item, Item)
        self.assertEqual(updated_item.name, "Ergonomic Monitor")
        self.assertEqual(
            updated_item.description,
            "High-quality monitor for professional work and bustle",
        )
        self.assertGreater(updated_item.price, item.price)

    def test_delete_item(self):
        item = self.item_repo.create_item(
            "Double Bass Headphones",
            "Noise-cancelling headphones for an immersive audio experience",
            99.99,
        )
        pre_del_item_count = self.item_repo.item_count
        self.item_repo.delete_item(item.sku)
        self.assertIsNone(self.item_repo.get_item(item_sku=item.sku))
        post_del_item_count = self.item_repo.item_count
        self.assertEqual(pre_del_item_count, post_del_item_count + 1)
        with self.assertRaises(ValueError):
            self.item_repo.delete_item(item_sku=item.sku)
