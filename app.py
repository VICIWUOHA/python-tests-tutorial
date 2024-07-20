from src.item import Item
from src.shopping_cart import ShoppingCart



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

print(item_2 == item_3)

import sqlite3
conn = sqlite3.connect('shop.db')
c = conn.cursor()
# create items table
c.execute("""CREATE TABLE IF NOT EXISTS items
             (name text, description text, price integer, sku text)""")
print("Table Created successfully.")

# insert items into table from item objects
c.execute("INSERT INTO items VALUES (:name, :description, :price, :sku)", 
          {'name': demo_item.name, 'description': demo_item.description, 'price': demo_item.price, 'sku': demo_item.sku})

c.execute("SELECT * FROM items")
print(c.fetchall())

from pytest_tests import test_ShoppingCart
