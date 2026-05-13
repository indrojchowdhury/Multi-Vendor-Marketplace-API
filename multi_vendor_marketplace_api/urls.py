from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    # Connect products app URLs to the main routing system
    path('api/products/', include('products.urls')),
]
