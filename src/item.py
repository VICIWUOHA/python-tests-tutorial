from dataclasses import dataclass, field
from pprint import pprint
import uuid
import logging


@dataclass
class Item:
    name: str
    description: str
    price: int
    sku: str = field(default_factory=lambda: str(uuid.uuid4()))

    # just overriding the default __str__ method
    def __str__(self) -> str:
        return str(
            {
                "name": self.name,
                "description": self.description,
                "price": self.price,
                "sku": self.sku,
            }
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            logging.warning(
                f"{other} is not an instance of `{self.__class__.__name__}`."
            )
            return False
        return self.sku == other.sku


class ItemRepository:
    def __init__(self) -> None:
        self.item_db: dict[str, Item] = {}

    def __item_exists(self, item: Item) -> bool:
        return item in self.item_db.values()

    def create_item(self, item: Item) -> None:
        self.item_db[f"{item.name}"] = item

    def get_item(self, item: Item) -> Item:
        return self.item_db[f"{item.name}"]

    def get_all_items(self) -> list[Item]:
        return list(self.item_db.values())

    def update_item(self, item: Item) -> None:
        pass

    def delete_item(self, item: Item) -> None:
        pass

    def add_item_to_db(self, item: dict) -> None:
        pprint(item)
