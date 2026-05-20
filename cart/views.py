from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create a cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check stock availability before adding to cart
        if product.stock < quantity:
            return Response({"error": f"Not enough stock. Available: {product.stock}"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the product already exists in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not item_created:
            # If item exists, update the quantity
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                return Response({"error": f"Cannot add more. Max available stock: {product.stock}"}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity = new_quantity
        else:
            # If it is a new item, set the initial quantity
            cart_item.quantity = quantity
            
        cart_item.save()
        return Response({"message": "Product added to cart successfully"}, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            # Find the cart item belonging to the logged-in user's cart
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)