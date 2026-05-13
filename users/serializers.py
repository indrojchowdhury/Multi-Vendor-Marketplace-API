from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    # password field is writen-only for security reasons
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone']

    def create(self, validated_data):
        # Create user using create_user method to handle password hashing automatically
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'buyer'),
            phone=validated_data.get('phone', '')
        )
        return user
