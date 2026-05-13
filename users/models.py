from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Define role choices for multi-vendor marketplace
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
