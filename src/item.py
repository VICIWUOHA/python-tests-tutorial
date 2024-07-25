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
    """
    An implementation class to manage CRUD ops for items in an e-commerce system using a SQLite database.

    Properties:
        `item_count` (int): Returns the number of existing items in the database.

    Methods:
        `create_item(name, description, price)`:
            Creates a new item and stores it in the database.
            Returns the created item object.
        `get_item(item_sku=None)`:
            Retrieves an item from the database by its SKU.
            If `item_sku` is not provided, returns all items.
        `get_all_items(limit=100)`:
            Retrieves all items from the database with an default limit of 100.
        `update_item(item)`:
            Updates an existing item in the database.
        `delete_item(item_sku)`:
            Deletes an item from the database by its SKU.
    """

    def __init__(self) -> None:
        self.__db_conn = sqlite3.connect("items.db")
        self.__db_cursor = self.__db_conn.cursor()
        self.__create_items_table()

    def __create_items_table(self) -> None:
        self.__db_cursor.execute("""CREATE TABLE IF NOT EXISTS items
                                 (sku VARCHAR PRIMARY KEY, name TEXT, description TEXT, price INTEGER);""")
        self.__db_conn.commit()

    def __item_exists(self, item_sku: str) -> bool:
        """
        Checks if an item exists in the db based on SKU.
        """
        self.__db_cursor.execute("SELECT 1 FROM items WHERE sku = ?", (item_sku,))
        return self.__db_cursor.fetchone() is not None

    def __add_item_to_db(self, item_dict: dict) -> bool:
        try:
            self.__db_cursor.execute(
                "INSERT INTO items VALUES (:sku, :name, :description, :price)",
                item_dict,
            )
            self.__db_conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"** Error while inserting item to db: {e}")
            return False

    @property
    def item_count(self) -> int:
        """
        Returns the number of existing items in the database.
        """
        return self.__db_cursor.execute("SELECT COUNT(1) FROM items").fetchone()[0]

    def create_item(self, name: str, description: str, price: int) -> Item:
        """
        Creates a new item and stores it in the database.
        Returns the created item object.
        """

        item = Item(name, description, price)
        if self.__item_exists(item.sku):
            raise ValueError(f"{item.sku} already exists.")

        if self.__add_item_to_db(item.__dict__):
            return item

    def get_item(self, item_sku: str = None) -> Item | None:
        """
        Retrieves an item from the database by its SKU.
        If `item_sku` is not provided, it raises an error.
        """

        if item_sku:
            self.__db_cursor.execute("SELECT * FROM items WHERE sku = ?", (item_sku,))
            item_data = self.__db_cursor.fetchone()
            return (
                Item(item_data[1], item_data[2], item_data[3], item_data[0])
                if item_data
                else None
            )
        raise KeyError("item_sku is required for the `get_item` call.")

    def get_all_items(self, limit: int = 100) -> list[Item]:
        """
        Retrieves all items from the database with an default limit of 100.
        """

        self.__db_cursor.execute(f"SELECT * FROM items LIMIT {limit}")
        items = self.__db_cursor.fetchall()
        if not items:
            return []
        return [Item(item[1], item[2], item[3], item[0]) for item in items]

    def update_item(self, item: Item) -> Item:
        """
        Updates an existing item in the database.
        Returns the updated item object.
        Raises a ValueError if a non-existing Item is supplied.
        """

        # check existence of item in db
        if self.__item_exists(item.sku):
            # update item in db
            self.__db_cursor.execute(
                "UPDATE items SET name = ?, description = ?, price = ? WHERE sku = ?",
                (item.name, item.description, item.price, item.sku),
            )
            self.__db_conn.commit()
            return self.get_item(item.sku)
        else:
            raise ValueError(f"Item `{item.sku}` does not exist in the database.")

    def delete_item(self, item_sku: str) -> None:
        """
        Deletes an item from the database by its SKU.
        Raises a ValueError if a non-existing Item is supplied.
        """
        if self.__item_exists(item_sku):
            self.__db_cursor.execute("DELETE FROM items WHERE sku = ?", (item_sku,))
            self.__db_conn.commit()
            return
        raise ValueError(f"Item `{item_sku}` does not exist in the database.")
