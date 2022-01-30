from decimal import Decimal

from products.domain.models import Money, Currency


class FakeCurrencyConverter:
    def exchange(self, money: Money, target_currency: Currency) -> Money:
        return Money(amount=Decimal(money.amount), currency=target_currency)
