import uuid
import requests
from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Fetch the user's cart
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the cart is empty
        if not cart.items.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Use transaction to ensure database integrity (All or Nothing)
        with transaction.atomic():
            #  Create the main order instance
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_price
            )

            #  Transfer cart items to order items and update product stock
            for cart_item in cart.items.all():
                product = cart_item.product

                # Final security check for stock availability
                if product.stock < cart_item.quantity:
                    return Response(
                        {"error": f"Not enough stock for {product.name}. Available: {product.stock}"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Deduct the quantity from product stock
                product.stock -= cart_item.quantity
                product.save()

                # Create OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    seller=product.seller,  # Link to the seller/vendor
                    price=product.price,    # Save current price
                    quantity=cart_item.quantity
                )

            #  Clear the cart after successfully placing the order
            cart.items.all().delete()

            serializer = OrderSerializer(order)
            return Response(
                {"message": "Order placed successfully", "order": serializer.data}, 
                status=status.HTTP_201_CREATED
            )


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            # Fetch the order that needs to be paid
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'Paid':
            return Response({"message": "This order is already paid"}, status=status.HTTP_400_BAD_REQUEST)

        # Set Base API URL dynamically based on Sandbox mode
        if settings.SSLCOMMERZ_IS_SANDBOX:
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
        else:
            api_url = "https://securepay.sslcommerz.com/gwprocess/v4/api.php"

        # Prepare payment data payload directly for SSLCommerz API
        post_data = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASS,
            'total_amount': str(order.total_amount),
            'currency': 'BDT',
            'tran_id': f"TXN-{order.id}-{uuid.uuid4().hex[:6].upper()}",
            'success_url': f"{settings.BASE_URL}/api/orders/payment/callback/?status=success&order_id={order.id}",
            'fail_url': f"{settings.BASE_URL}/api/orders/payment/callback/?status=fail&order_id={order.id}",
            'cancel_url': f"{settings.BASE_URL}/api/orders/payment/callback/?status=cancel&order_id={order.id}",
            'emi_option': 0,
            'cus_name': request.user.username,
            'cus_email': request.user.email if request.user.email else "test@example.com",
            'cus_phone': "01700000000",
            'cus_add1': "Dhaka, Bangladesh",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "No",
            'num_of_item': 1,
            'product_name': f"Order #{order.id}",
            'product_category': "E-commerce",
            'product_profile': "general"
        }

        try:
            # Send Direct HTTP POST request to SSLCommerz Server
            response = requests.post(api_url, data=post_data)
            response_data = response.json()
        except Exception as e:
            return Response({"error": f"API Connection error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check API response status
        if response_data.get('status') == 'SUCCESS':
            return Response({"GatewayPageURL": response_data.get('GatewayPageURL')}, status=status.HTTP_200_OK)
        else:
            error_msg = response_data.get('failedreason', 'Unknown error from SSLCommerz')
            return Response({"error": f"Payment failed. Reason: {error_msg}"}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentCallbackView(APIView):
    permission_classes = [AllowAny]  # SSLCommerz server will send data without JWT token

    def post(self, request):
        payment_status = request.query_params.get('status')
        order_id = request.query_params.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if payment_status == 'success':
            order.status = 'Paid'
            order.save()
            return Response({"message": "Payment successful! Order updated to Paid."}, status=status.HTTP_200_OK)
            
        elif payment_status == 'fail':
            order.status = 'Cancelled'
            order.save()
            return Response({"message": "Payment failed! Order updated to Cancelled."}, status=status.HTTP_200_OK)
            
        else:
            return Response({"message": "Payment cancelled by user."}, status=status.HTTP_200_OK)