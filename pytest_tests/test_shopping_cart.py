from src.shopping_cart import ShoppingCart
from src.item import Item
import pytest


@pytest.fixture(scope="session")
def shopping_cart() -> ShoppingCart:
    my_cart = ShoppingCart("Ewolo")
    return my_cart

@pytest.fixture(scope="session")
def item():
    return Item("Foozie Ergonomic Mouse", "Comfy Mouse for gamers", 50).__dict__

# @pytest.mark.usefixtures(shopping_cart)  enables the fixture but doesn't pass it into the fxn
def test_add_items_to_cart(shopping_cart: ShoppingCart, item: Item):
    shopping_cart.add_item(
        item, 40
    )
    assert shopping_cart.cart_size == 1


def test_remove_item_from_cart(shopping_cart: ShoppingCart, item: Item):
    shopping_cart.add_item(
        item, 40
    )
    shopping_cart.remove_cart_item(
        item
    )
    assert shopping_cart.cart_size == 0


@pytest.mark.skip(reason="Not Implemented Yet")
def test_reduce_nonexistent_item_from_cart(shopping_cart: ShoppingCart):
    shopping_cart.add_item(
        Item("Foozie Ergonomic Mouse", "Comfy Mouse for gamers", 50).item(), 40
    )
    shopping_cart.remove_cart_item(
        Item("Foozie Ergonomic Mouse", "Comfy Mouse for gamers", 50).item()
    )
    assert shopping_cart.cart_size == 0
