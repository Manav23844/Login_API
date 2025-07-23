from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from .serializers import (
    UserRegistrationSerializer,
    OTPRequestSerializer,
    OTPVerificationSerializer
)
from .utils import OTPService
from .models import OTP
from django.http import HttpResponse

User = get_user_model()

def home(request):
    return HttpResponse("Welcome to the OTP Auth Project!")

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    # Example logic, replace with your registration logic
    return Response({"message": "User registered successfully!"})

@api_view(['POST'])
@permission_classes([AllowAny])
def request_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required.'}, status=400)
    # Here you would generate and send the OTP to the email
    # For now, just return a success message
    return Response({'message': 'OTP sent to your email.'})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    if not email or not otp:
        return Response({'error': 'Email and OTP are required.'}, status=400)
    # Here you would verify the OTP for the email
    # For now, just return a success message and a dummy token
    return Response({
        'message': 'Login successful.',
        'token': 'jwt_token'
    })

@api_view(['GET'])
def profile(request):
    """
    Get user profile (requires authentication)
    """
    return Response({
        'user': {
            'email': request.user.email,
            'is_email_verified': request.user.is_email_verified,
            'date_joined': request.user.date_joined
        }
    })

@api_view(['POST'])
def logout(request):
    """
    Logout user by blacklisting refresh token
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Successfully logged out.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Logout failed.'
        }, status=status.HTTP_400_BAD_REQUEST)