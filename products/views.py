from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product
from .serializers import ProductSerializer

# Custom permission to allow only sellers to create/modify products
class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'seller'

# Custom permission to ensure only the owner of the product can modify or delete it
class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user

# --- THIS WAS MISSING OR OVERWRITTEN ---
class ProductListCreateView(APIView):
    permission_classes = [IsSeller]

    # Get list of all products (Public API)
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new product (Only for logged-in sellers)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProductOwner]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    # Update product details (PUT method)
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, product)
        
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete product (DELETE method)
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, product)
        
        product.delete()
        return Response({"message": "Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
