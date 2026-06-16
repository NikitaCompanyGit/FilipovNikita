from decimal import Decimal

import pytest

from generated_code import fibonacci, is_prime, normalize_phone
from refactored_code import ShoppingBag, ProductRecord, create_bag_from_raw


def test_shopping_bag_total_and_search():
    bag = create_bag_from_raw(
        [
            {"name": "Notebook", "price": "75000", "qty": 1},
            {"name": "Mouse", "price": "1500", "qty": 2},
        ]
    )

    assert bag.get_grand_total() == Decimal("78000")
    assert bag.search_item_by_name("mouse") == ProductRecord("Mouse", Decimal("1500"), 2)
    assert bag.search_item_by_name("keyboard") is None


def test_shopping_bag_invalid_records():
    bag = ShoppingBag()

    with pytest.raises(ValueError):
        bag.add_product(ProductRecord("InvalidItem", Decimal("100"), 0))

    with pytest.raises(ValueError):
        bag.add_product(ProductRecord("InvalidPrice", Decimal("-10"), 2))


def test_generated_utilities():
    assert is_prime(2)
    assert is_prime(97)
    assert not is_prime(1)
    assert not is_prime(100)
    assert fibonacci(7) == [0, 1, 1, 2, 3, 5, 8]
    assert normalize_phone("8 (999) 123-45-67") == "+79991234567"
