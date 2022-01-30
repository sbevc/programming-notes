from django.shortcuts import render

from products.services import ProductService


def list_products(request):
    products = ProductService().get_featured_products()
    return render(request, "products/list.html", {"products": products})