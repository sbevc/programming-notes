from __future__ import annotations
import typing
from dataclasses import dataclass
from decimal import Decimal


class UserContext(typing.Protocol):
    @property
    def is_preferred(self) -> bool:
        raise NotImplementedError

    @property
    def currency(self) -> Currency:
        raise NotImplementedError


@dataclass
class Product:
    name: str
    unit_price: Money
    is_featured: bool

    def apply_discount_for(self, user: UserContext):
        discount = 0.95 if user.is_preferred else 1
        return DiscountedProduct(name=self.name, unit_price=self.unit_price * discount)


@dataclass
class DiscountedProduct:
    name: str
    unit_price: Money


@dataclass
class Money:
    amount: Decimal
    currency: Currency

    def __mul__(self, number):
        return Money(amount=self.amount * number, currency=self.currency)

    def __str__(self):
        return f"{self.amount}{self.currency}"


@dataclass
class Currency:
    code: str

    def __str__(self):
        return self.code
