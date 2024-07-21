from src.shopping_cart import ShoppingCart
from src.item import Item
import pytest

# Here we  define the  fixtures for the  tests
# Pytest would parse them when we run our tests


@pytest.fixture(scope="session")
def shopping_cart() -> ShoppingCart:
    my_cart = ShoppingCart("Ewolo")
    return my_cart


@pytest.fixture(scope="session")
def item():
    return Item(
        name="Foozie Ergonomic Mouse", description="Comfy Mouse for gamers", price=50
    ).__dict__
