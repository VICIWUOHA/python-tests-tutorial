import unittest
from src.item import Item


class TestItem(unittest.TestCase):
    def test_item_price_cannot_be_negative(self):
        # our item class should raise a ValueError if the price is below zero
        with self.assertRaises(ValueError):
            Item("External SSD", "High-speed storage for data transfer", -5.0)
