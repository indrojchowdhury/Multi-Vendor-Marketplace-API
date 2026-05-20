from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

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

class ProductListCreateView(APIView):
    permission_classes = [IsSeller]
    
    # Configure filter, search, and ordering backends for this view
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stock']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    # Get list of all products (Public API with Pagination)
    def get(self, request):
        # Fetch all products ordered by id for consistent pagination
        products = Product.objects.all().order_by('id')
        
        # Apply filtering, searching, and sorting to the queryset sequentially
        for backend in list(self.filter_backends):
            products = backend().filter_queryset(request, products, self)
        
        # Initialize the page number paginator
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(products, request)
        
        # If pagination is active for this request, return the paginated response
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Fallback response if pagination fails
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
