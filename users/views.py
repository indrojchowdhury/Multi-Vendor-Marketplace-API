from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class RegisterView(APIView):
    # Handle POST request for user registration
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        # Check if the sent data matches model rules and validation
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!", "user": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        
        # Return validation errors if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
