import typing

from django.shortcuts import render
from django.views import View

from .models import FeaturedProductsViewModel, ProductViewModel
from ..domain.models import DiscountedProduct


class IProductService(typing.Protocol):
    def get_featured_products(self, user) -> list[DiscountedProduct]:
        pass


class IndexView(View):
    # Have to declare the dependency
    product_service: IProductService = None

    # This is not necessary but the dependency is more straight forward
    def __init__(self, product_service: IProductService):
        self.product_service = product_service

    def get(self, request):
        prods = self.product_service.get_featured_products(user=request.user)
        pvm = FeaturedProductsViewModel([
            ProductViewModel(p.name, p.unit_price) for p in prods
        ])
        return render(request, "products/list.html", {"products_view_model": pvm})
