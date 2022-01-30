import typing

from products.repositories import ProductRepository

from products.domain.models import DiscountedProduct, Money, Currency


class CurrencyConverter(typing.Protocol):
    def exchange(self, money: Money, target_currency: Currency) -> Money:
        pass


class ProductService:
    def __init__(self, products_repository: ProductRepository, converter: CurrencyConverter):
        self.products_repository = products_repository
        self.converter = converter

    def get_featured_products(self, user) -> list[DiscountedProduct]:
        prods = self.products_repository.get_featured_products()
        for prod in prods:
            prod.unit_price = self.converter.exchange(prod.unit_price, user.currency)
        return [prod.apply_discount_for(user) for prod in self.products_repository.get_featured_products()]
