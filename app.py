from src.item_repository import ItemRepository
from src.item import Item
from src.shopping_cart import ShoppingCart

##### Dummy Script for testing App Functionality



demo_item = Item(
    name="Double Bass Headset",
    description="This is a double bass headset brought to you by Vic technologies.",
    price=100,
)

demo_item_2 = Item(
    name="Demo Item 2",
    description="This is a demo item 2",
    price=200,
)

item_3 = demo_item_2

# check equality
print(item_3 == demo_item)
# check other type comparison
print(item_3 == "demo_item")

my_Cart = ShoppingCart("Ewolo")
print(my_Cart.add_item(demo_item,10))
print(my_Cart.show_cart)
print(my_Cart.reduce_cart_item_quantity(demo_item, 2))
print(my_Cart.show_cart)
print(my_Cart.remove_cart_item(demo_item))