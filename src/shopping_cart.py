from datetime import datetime as dt
from src.item import Item
import uuid
import json
from enum import Enum


class ShoppingCart:
    """Shopping Cart Class

    Args:
        `user_id (str)`: Owner of the cart.


    Properties:
        cart_size: returns the number of items in the cart
        show_cart: returns a json string of the cart

    Methods:

        `add_item`: adds an item to the cart
        `remove_cart_item`: removes an item from the cart
        `increase_cart_item_quantity`: increases the quantity of an item in the cart if it exists or adds it of not.
        `decrease_cart_item_quantity`: decreases the quantity of an item in the cart
        `reset_cart`: resets the cart to a clear state.
    """

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
        return json.dumps(
            {"cart_id": self.cart_id, "cart_items": self.cart_obj}, indent=4
        )

    def reset_cart(self):
        self.cart_obj = {}
        print(f"==> Cart `{self.cart_id}` has been reset.")

    def __item_in_cart(self, item: Item):
        item_sku = item.sku
        if item_sku in self.cart_obj:
            print(f"Item `{item.name}` already in cart.")
            return True
        return False

    def add_item(self, item: Item, quantity: int):
        # check if item exists in cart , then update

        if self.__item_in_cart(item):
            self.increase_cart_item_quantity(item, quantity)
        else:
            # add new item using it's __dict__ property for easy access
            self.cart_obj[f"{item.sku}"] = {
                "item": item.__dict__,
                "quantity": quantity,
                "added_at": dt.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                "updated_at": dt.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            }
            print(f"==>> `{item.name}` Added to Cart.")
            return json.dumps(
                {
                    "status": ShoppingCartStatus.CART_ITEM_ADDED.value,
                    f"{item.name}": self.cart_obj[f"{item.sku}"],
                },
                indent=4,
            )

    def remove_cart_item(self, item: Item):
        self.cart_obj.pop(f"{item.sku}", "Item Not Found In Cart.")
        return json.dumps(
            {
                "status": ShoppingCartStatus.CART_ITEM_REMOVED.value,
                "item": item.__dict__,
            },
            indent=4,
        )

    def increase_cart_item_quantity(self, item: Item, quantity: int):
        # check if item exists
        if self.__item_in_cart(item):
            cart_item_details = self.cart_obj[f"{item.sku}"]
            cart_item_details["quantity"] += quantity
            cart_item_details["updated_at"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            return json.dumps(
                {
                    "status": ShoppingCartStatus.CART_ITEM_UPDATED.value,
                    f"{item.name}": self.cart_obj[f"{item.sku}"],
                },
                indent=4,
            )
        else:
            # we shouldn't be able to update non-existing items stock in cart
            raise Exception("ItemNotFound", f"Item {item.name} not in cart.")

    def reduce_cart_item_quantity(self, item: Item, quantity):
        # check if item exists
        if self.__item_in_cart(item):
            cart_item_details = self.cart_obj[f"{item.sku}"]
            if cart_item_details["quantity"] <= quantity:
                # not the best impl, but this means a reduction to zero or less, hence remove item from cart.
                return self.remove_cart_item(item)
            cart_item_details["quantity"] -= quantity
            cart_item_details["updated_at"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            return json.dumps(
                {
                    "status": ShoppingCartStatus.CART_ITEM_UPDATED.value,
                    f"{item.name}": self.cart_obj[f"{item.sku}"],
                },
                indent=4,
            )
        else:
            # we shouldn't be able to update non-existing items stock in cart
            raise Exception("ItemNotFound", f"Item {item.name} not in Cart.")


class ShoppingCartStatus(Enum):
    """Handles different Statuses which we can encounter within our Shoping Cart"""

    # Arguably we can embed this in the ShoppingCart Class, but let's keep it separate for now.

    CART_CREATED = "CartCreated"
    CART_ITEM_ADDED = "CartItemAdded"
    CART_ITEM_REMOVED = "CartItemRemoved"
    CART_ITEM_UPDATED = "CartItemUpdated"


#  See sample Shopping Flow in app.py
