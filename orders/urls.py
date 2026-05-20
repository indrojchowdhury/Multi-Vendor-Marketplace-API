from django.urls import path
from .views import CreateOrderView, InitiatePaymentView, PaymentCallbackView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('payment/initiate/<int:order_id>/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payment/callback/', PaymentCallbackView.as_view(), name='payment-callback'),
]