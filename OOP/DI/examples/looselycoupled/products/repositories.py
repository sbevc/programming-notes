import typing

from .domain.models import Product
from .models import ProductDTO


class ProductRepository(typing.Protocol):
    def get_featured_products(self) -> list[Product]:
        pass


class DjangoProductRepository:
    def get_featured_products(self) -> list[Product]:
        return [p.to_domain() for p in ProductDTO.objects.filter(is_featured=True)]
