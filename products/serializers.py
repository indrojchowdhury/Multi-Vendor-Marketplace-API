from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # Make seller field read-only because we will assign it automatically from the logged-in user
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'price', 'stock', 'created_at']
