from .models import ProductDTO


class ProductService:
    def get_featured_products(self) -> list[ProductDTO]:
        return ProductDTO.objects.filter(is_featured=True)