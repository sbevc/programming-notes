from django.db import models


class ProductDTO(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    is_featured = models.BooleanField(null=False)
