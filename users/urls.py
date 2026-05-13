from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    # API path for user registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # API path for user login (Generates access and refresh tokens)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # API path to get a new access token using refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
