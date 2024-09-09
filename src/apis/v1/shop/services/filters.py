from typing import Sequence

from .....models.products import Product


class ProductFilter:
    @staticmethod
    def filter_by_categories(products: list[Product] | Sequence[Product], categories: list[str]) -> list[Product]:
        return [
            item
            for item in products
            if item.categories
            and set(map(lambda x: x.name.lower(), item.categories)).intersection(categories)
        ]
