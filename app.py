from src.item_repository import ItemRepository
from src.item import Item
from src.shopping_cart import ShoppingCart

##### Dummy Script for testing App Functionality



demo_item = Item(
    name="Demo Item",
    description="This is a demo item",
    price=100,
)


item_2 = Item(
    name="Demo Item 2",
    description="This is a demo item 2",
    price=200,
)

item_3 = item_2

print(item_3 == demo_item)

import sys
print(sys.path)