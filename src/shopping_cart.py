from datetime import datetime as dt
from src.item import Item
import uuid
import json
from enum import Enum


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
        return json.dumps({"cart_id": self.cart_id, "cart_items": self.cart_obj},indent=4)

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
            return json.dumps({
                "status": ShoppingCartStatus.CART_ITEM_ADDED.value,
                f"{item.name}": self.cart_obj[f"{item.sku}"],
            },indent=4)

    def remove_cart_item(self, item: Item):
        self.cart_obj.pop(f"{item.sku}", "Item Not Found In Cart.")
        return json.dumps({"status": ShoppingCartStatus.CART_ITEM_REMOVED.value, "item": item.__dict__},indent=4)

    def increase_cart_item_quantity(self, item:Item, quantity:int):
        # check if item exists
        if self.__item_in_cart(item):
            cart_item_details = self.cart_obj[f"{item.sku}"]
            cart_item_details["quantity"] += quantity
            cart_item_details["updated_at"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            return json.dumps({
                "status": ShoppingCartStatus.CART_ITEM_UPDATED.value,
                f"{item.name}": self.cart_obj[f"{item.sku}"],
            },indent=4)
        else:
            # we shouldn't be able to update non-existing items stock in cart
            raise Exception("ItemNotFound", f"Item {item.name} not in cart.")

    def reduce_cart_item_quantity(self, item:Item, quantity):
        # check if item exists
        if self.__item_in_cart(item):
            cart_item_details = self.cart_obj[f"{item.sku}"]
            if cart_item_details["quantity"] <= quantity:
                # not the best impl, but this means a reduction to zero or less, hence remove item from cart.
                return self.remove_cart_item(item)
            cart_item_details["quantity"] -= quantity
            cart_item_details["updated_at"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            return json.dumps({
                "status": ShoppingCartStatus.CART_ITEM_UPDATED.value,
                f"{item.name}": self.cart_obj[f"{item.sku}"],
            },indent=4)
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
