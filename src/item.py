from dataclasses import dataclass, field
import uuid
import logging


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
