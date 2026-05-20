from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    # Link each cart to a unique user
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        # Calculate the total price of all items in the cart
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    # Link items to the main cart
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        # Calculate the total price for this specific item (price * quantity)
        return self.product.price * self.quantity