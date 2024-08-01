from datetime import datetime as dt
from src.item import Item
import uuid
import json


class ShoppingCart:
    def __init__(self, user_id: str) -> None:
        self.cart_owner = user_id
        self.cart_id = str(uuid.uuid4())
        self.cart_creation_time = dt.now()
        self.cart_container = []
        self.cart_obj = {}
        print(
            f" ==>>>> Hello {self.cart_owner} Your New Cart ->(`{self.cart_id}`) was Created at `{self.cart_creation_time}`."
        )

    @property
    def cart_size(self):
        return len(self.cart_obj)

    @property
    def show_cart(self):
        return json.dumps({"cart_id": self.cart_id, "cart_items": self.cart_obj})

    def __item_in_cart(self, item: Item):
        item_sku = item["name"]
        if item_sku in self.cart_obj:
            print(f"Item `{item['name']}` already in cart.")
            return True
        return False

    def add_item(self, item: Item, quantity: int):
        # check if item exists in cart , then update

        if self.__item_in_cart(item):
            self.increase_cart_item_quantity(item, quantity)
        else:
            # add new item
            item["quantity"] = quantity
            self.cart_obj[f"{item['name']}"] = item
            print(f"==>> {item['name']} Added to Cart.")
            return {
                "status": "CartItemAdded",
                f"{item['name']}": self.cart_obj[f"{item['name']}"],
            }

    def remove_cart_item(self, item: Item):
        self.cart_obj.pop(f"{item['name']}", "Item Not Found In Cart.")

        return {"status": "CartItemRemoved", "Item": item}

    def increase_cart_item_quantity(self, item, quantity):
        # check if item exists
        if self.__item_in_cart(item):
            cart_item_details = self.cart_obj[f"{item['name']}"]
            cart_item_details["quantity"] += quantity

            return {
                "status": "CartItemUpdated",
                f"{item['name']}": self.cart_obj[f"{item['name']}"],
            }
        else:
            # we shouldn't be able to update non-existing items stock in cart
            raise Exception("ItemNotFound", f"Item {item['name']} not in cart.")

    def reduce_cart_item_quantity(self, item, quantity):
        # check if item exists
        if self.__item_in_cart(item):
            cart_item_details = self.cart_obj[f"{item['name']}"]
            if cart_item_details["quantity"] == quantity:
                # this means a reduction to zero, hence remove item from cart.
                return self.remove_cart_item(item)
            cart_item_details["quantity"] -= quantity

            return {
                "status": "CartItemUpdated",
                f"{item['name']}": self.cart_obj[f"{item['name']}"],
            }
        else:
            # we shouldn't be able to update non-existing items stock in cart
            raise Exception("ItemNotFound", f"Item {item['name']} not in Cart.")


# mouse = Item("Foozie Ergonomic Mouse", "Comfy Mouse for gamers", 50).item()
# pprint(speaker_item)
# my_Cart = ShoppingCart("Ewolo")
# my_Cart.add_item(speaker_item, 4)
# my_Cart.add_item(mouse, 40)
# pprint(my_Cart.cart_size)
# pprint(my_Cart.show_cart)
# pprint(my_Cart.increase_cart_item_quantity(speaker_item, 3))
# pprint(my_Cart.reduce_cart_item_quantity(speaker_item, 3))
# pprint(my_Cart.show_cart)
# pprint(my_Cart.reduce_cart_item_quantity(speaker_item, 4))
# pprint(my_Cart.show_cart)
# pprint(my_Cart.reduce_cart_item_quantity(speaker_item, 4))
