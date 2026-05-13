from django.urls import path
from .views import ProductListCreateView, ProductUpdateDeleteView

urlpatterns = [
    # API path for creating a new product
    path('create/', ProductListCreateView.as_view(), name='product-create'),
    
    # API path for updating a product (Requires Product ID, e.g., /update/1/)
    path('update/<int:pk>/', ProductUpdateDeleteView.as_view(), name='product-update'),
    
    # API path for deleting a product (Requires Product ID, e.g., /delete/1/)
    path('delete/<int:pk>/', ProductUpdateDeleteView.as_view(), name='product-delete'),
]
