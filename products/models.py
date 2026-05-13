from django.db import models
from django.conf import settings

class Product(models.Model):
    # Link each product to a seller (User model)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.seller.username}"
