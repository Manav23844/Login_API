from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP
import re

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = ['email']
    
    def validate_email(self, value):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Invalid email format.")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        
        return value.lower()
    
    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0] + str(User.objects.count() + 1)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            is_active=True
        )
        return user

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value.lower()

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value.lower()
    
    def validate_otp(self, value):
        if len(value) != 6 or not value.isdigit():
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return value
