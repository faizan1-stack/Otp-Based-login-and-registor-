from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .renderer import UserRenderer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import *

user = get_user_model()
def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_user_instance(self, data):
        try:
             return User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            return None


class RegisterView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            otp = generate_otp()
            user.otp_expires_at = timezone.now() + timezone.timedelta(minutes=1)
            user.max_otp_attempts = 3
            user.otp = otp
            user.otp_created_at = timezone.now() 
            user.save()

            if send_otp_email(user, otp):
                return Response({
                    'message': 'User created successfully. OTP sent to your email. Please verify.',
                    'user_id': user.id,
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'User created, but failed to send OTP. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({
            'error': 'Registration does not support GET method.'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class LoginView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_tokens_for_user(user)
        return Response({
            'token' : token,
            'message' : 'Login Sucessfully',
        }, status=status.HTTP_201_CREATED)
    

class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self , request , format=None , **kwargs) :
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data ,status=status.HTTP_202_ACCEPTED)

class ResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request ,format=None):
        user = request.user
        serializer = ResetPasswordSerializer(data = request.data , context={'user' : request.user})
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']    
            if not user.check_password(old_password):
                return Response({
                    'error' : 'your old password is not corrrected'
                } , status=status.HTTP_401_UNAUTHORIZED)
            if new_password != confirm_password:
                return Response({
                    'error': 'your new password is not match with confirm password'
                } , status=status.HTTP_403_FORBIDDEN )
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OtpView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post (self , request , format = None):
        serializer = OTPVerifySerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            if user is None:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            if user.is_email_verified:
                return Response({'message': 'Email is already verified'}, status=status.HTTP_200_OK)
            if user.otp != serializer.validated_data['otp']:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            if user.otp_expires_at < timezone.now():
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.is_email_verified = True
            user.otp = None
            user.created_at = None
            user.otp_expires_at = None
            user.max_otp_attempts = 3
            user.otp_max_out = None
            user.save()
            return Response({
                'message': 'Email verified successfully'},
                 status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class ResendOtpView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        if user.is_email_verified:
            return Response({'message': 'Email is already verified'}, status=status.HTTP_200_OK)
           
        if user.otp_max_out and user.max_otp_attempts <= 0 and user.otp_max_out > timezone.now():
            return Response({'error': 'Maximum OTP attempts exceeded. Please try again later.'}, status=status.HTTP_403_FORBIDDEN)
           
        otp = generate_otp()
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.otp_expires_at = timezone.now() + timedelta(minutes=1)
        user.max_otp_attempts = 3
        user.otp_max_out = None
        user.save()
           
        if send_otp_email(user, otp):
            return Response({'message': 'OTP resent successfully. Please check your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to send OTP. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]       
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']    
            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_password:
                return Response({"error": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successfully logged out. Token blacklisted."},
            status=200
        )