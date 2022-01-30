from django.db import models
from django.contrib.auth.models import AbstractUser

from products.domain.models import Product, Currency, Money


class ProductDTO(models.Model):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=5)
    is_featured = models.BooleanField()

    def to_domain(self) -> Product:
        return Product(
            name=self.name,
            unit_price=Money(self.unit_price, Currency(self.currency)),
            is_featured=self.is_featured
        )


class MyUser(AbstractUser):
    @property
    def is_preferred(self):
        return False


class AnonymousUser:
    @property
    def is_preferred(self):
        return False

    @property
    def currency(self):
        return Currency("USD")
