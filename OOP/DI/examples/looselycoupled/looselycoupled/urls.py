"""looselycoupled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dependencies import Injector

from products.adapters.currency_converter import FakeCurrencyConverter
from products.views.views import IndexView
from products.repositories import DjangoProductRepository
from products.domain.services import ProductService


# Build dependencies with "Pure DI"
repo = DjangoProductRepository()
converter = FakeCurrencyConverter()
product_service = ProductService(repo, converter)


# Using a DI Container
class Container(Injector):
    products_repository = DjangoProductRepository
    converter = FakeCurrencyConverter
    product_service = ProductService


urlpatterns = [
    path('admin/', admin.site.urls),

    # Using pure DI
    path("", IndexView.as_view(product_service=product_service), name="index"),

    # Using a DI Container
    path("", IndexView.as_view(product_service=Container.product_service), name="index"),
]
