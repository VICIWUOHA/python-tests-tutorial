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

    Attributes:
        `item_count` (int): The number of items in the repository.
        `_db_conn` (sqlite3.Connection): The connection to the SQLite database.
        `_db_cursor` (sqlite3.Cursor): The cursor object for executing SQL queries.
        `item_db` (dict[str, Item]): A dictionary to store items, keyed by their SKU.

    Methods:
        `create_item(name, description, price)`:
            Creates a new item and stores it in the database.
            Returns the created item object.
        `get_item(item_sku=None)`:
            Retrieves an item from the database by its SKU.
            If `item_sku` is not provided, returns all items.
        `update_item(item)`:
            Updates an existing item in the database.
        `delete_item(item_sku)`:
            Deletes an item from the database by its SKU.
    """

    def __init__(self) -> None:
        self.item_count: int = 0
        self._db_conn = sqlite3.connect("items.db")
        self._db_cursor = self._db_conn.cursor()
        self.__create_items_table()
        
    def __create_items_table(self) -> None:
        self._db_cursor.execute("""CREATE TABLE IF NOT EXISTS items
                                 (sku VARCHAR PRIMARY KEY, name TEXT, description TEXT, price INTEGER);""")
        self._db_conn.commit()

    def __item_exists(self, item_sku: str) -> bool:
        """
        Checks if an item exists in teh db based on SKU.
        """
        self._db_cursor.execute("SELECT 1 FROM items WHERE sku = ?", (item_sku,))
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
        if self.__item_exists(item.sku):
            raise ValueError(f"{item.sku} already exists.")

        if self.__add_item_to_db(item.__dict__):
            self.item_count += 1
            return item

    def get_item(self, item_sku: str = None) -> Item | None:
        if item_sku:
            self._db_cursor.execute("SELECT * FROM items WHERE sku = ?", (item_sku,))
            item_data = self._db_cursor.fetchone()
            return (
                Item(item_data[0], item_data[1], item_data[2], item_data[3])
                if item_data
                else None
            )
        raise KeyError("item_sku is required for the `get_item` call.")

    def get_all_items(self, limit:int=100) -> list[Item]:
        self._db_cursor.execute(f"SELECT * FROM items LIMIT {limit}")
        items = self._db_cursor.fetchall()
        if not items:
            return []
        return [Item(item[0], item[1], item[2], item[3]) for item in items]
        

    def update_item(self, item: Item) -> None:
        # check existence of item in db
        if self.__item_exists(item.sku):
            # update item in db
            self._db_cursor.execute(
                "UPDATE items SET name = ?, description = ?, price = ? WHERE sku = ?",
                (item.name, item.description, item.price, item.sku),
            )
            self._db_conn.commit()
            return self.get_item(item.sku)
        else:
            raise ValueError(f"Item `{item.sku}` does not exist in the database.")


    def delete_item(self, item_sku: str) -> None:
        if self.__item_exists(item_sku):
            self._db_cursor.execute("DELETE FROM items WHERE sku = ?", (item_sku, ))
            self._db_conn.commit()
            self.item_count -= 1
            return
        raise ValueError(f"Item `{item_sku}` does not exist in the database.")

