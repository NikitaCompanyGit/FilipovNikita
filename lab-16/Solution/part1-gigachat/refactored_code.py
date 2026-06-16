"""Refactored shopping cart utilities created and verified for lab 16."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True)
class ProductRecord:
    title: str
    price_val: Decimal
    qty_count: int

    @classmethod
    def load_from_map(cls, data_map: dict) -> "ProductRecord":
        return cls(
            title=str(data_map["name"]),
            price_val=Decimal(str(data_map["price"])),
            qty_count=int(data_map["qty"]),
        )

    @property
    def cost(self) -> Decimal:
        return self.price_val * self.qty_count


class ShoppingBag:
    def __init__(self, items: Iterable[ProductRecord] | None = None):
        self._contents = list(items or [])

    @property
    def contents(self) -> tuple[ProductRecord, ...]:
        return tuple(self._contents)

    def add_product(self, item: ProductRecord) -> None:
        if item.qty_count <= 0:
            raise ValueError("Quantity must be positive and greater than zero")
        if item.price_val <= 0:
            raise ValueError("Price must be positive and greater than zero")
        self._contents.append(item)

    def get_grand_total(self) -> Decimal:
        return sum((item.cost for item in self._contents), Decimal("0"))

    def search_item_by_name(self, query_name: str) -> ProductRecord | None:
        lowered_query = query_name.strip().casefold()
        for item in self._contents:
            if item.title.strip().casefold() == lowered_query:
                return item
        return None


def create_bag_from_raw(records: Iterable[dict]) -> ShoppingBag:
    bag = ShoppingBag()
    for row in records:
        bag.add_product(ProductRecord.load_from_map(row))
    return bag
