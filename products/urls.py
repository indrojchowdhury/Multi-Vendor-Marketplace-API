from django.urls import path
from .views import ProductListCreateView, ProductUpdateDeleteView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('update/<int:pk>/', ProductUpdateDeleteView.as_view(), name='product-update'),
    path('delete/<int:pk>/', ProductUpdateDeleteView.as_view(), name='product-delete'),
]
