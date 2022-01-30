from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductViewModel:
    name: str
    unit_price: Decimal

    @property
    def summary_text(self):
        return f"{self.name} {self.unit_price}"


@dataclass
class FeaturedProductsViewModel:
    products: list[ProductViewModel]