from dataclasses import dataclass, field
import uuid
import logging
import sqlite3


@dataclass
class Item:
    """
    Represents a sample item in an e-commerce system.

    Attributes:
        `name` (str): The name of the item.
        `description` (str): A brief description of the item.
        `price` (int): The price of the item in USD.
        `sku` (str): A unique stock-keeping unit (SKU) for the item, generated automatically. 
                     Note that this can be delegated to the database engine in prod use cases.

    """

    name: str
    description: str
    price: int
    sku: str = field(default_factory=lambda: str(uuid.uuid4()))

    # just overriding the default __str__ method
    def __str__(self) -> str:
        return str(
            {
                "sku": self.sku,
                "name": self.name,
                "description": self.description,
                "price": self.price,
            }
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            logging.warning(
                f"{other} is not an instance of `{self.__class__.__name__}`."
            )
            return False
        return self.sku == other.sku

    # Added to ensure our items never have a -ve price.
    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f"Item Price cannot be a negative value: {self.price}")


class ItemRepository:
    def __init__(self) -> None:
        self.item_count: int = 0
        self._db_conn = sqlite3.connect("items.db")
        self._db_cursor = self._db_conn.cursor()
        self.__create_items_table()
        self.item_db: dict[str, Item] = {}

    def __create_items_table(self) -> None:
        self._db_cursor.execute("""CREATE TABLE IF NOT EXISTS items
                                 (sku VARCHAR PRIMARY KEY, name TEXT, description TEXT, price INTEGER);""")
        self._db_conn.commit()

    def __item_exists(self, item: Item) -> bool:
        self._db_cursor.execute("SELECT 1 FROM items WHERE sku = ?", (item.sku,))
        return self._db_cursor.fetchone() is not None

    def __add_item_to_db(self, item_dict: dict) -> bool:
        try:
            self._db_cursor.execute(
                "INSERT INTO items VALUES (:sku, :name, :description, :price)",
                item_dict,
            )
            self._db_conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"** Error while inserting item to db: {e}")
            return False

    def create_item(self, name, description, price) -> Item:
        item = Item(name, description, price)
        if self.__item_exists(item):
            raise ValueError(f"{item.sku} already exists.")

        if self.__add_item_to_db(item.__dict__):
            self.item_count += 1

            return item

    def get_item(self, item_sku: str = None) -> Item | None:
        if item_sku:
            self._db_cursor.execute("SELECT * FROM items WHERE sku = ?", (item_sku,))
            item_data = self._db_cursor.fetchone()
            return (
                Item(item_data[1], item_data[2], item_data[3], item_data[0])
                if item_data
                else None
            )

        raise KeyError("item_sku is required for the `get_item` call")

    def get_all_items(self) -> list[Item]:
        pass

    def update_item(self, item: Item) -> None:
        pass

    def delete_item(self, item: Item) -> None:
        pass
