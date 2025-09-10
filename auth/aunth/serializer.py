from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from random import randint
from django.utils import timezone

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta: 
        model = User
        fields = ['email' , 'username' , 'phone_number' , 'password' , 'password2']
        extra_kwargs = {'password': {'write_only': True}}
        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            if len(attrs['password']) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long")
            return attrs
        
    def create(self ,validated_data , *args , **kwargs):
        user = User.objects.create_user(
                email = validated_data['email'],
                username = validated_data['username'],
                phone_number = validated_data['phone_number'],
                
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email' , 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if  not email or not password:
            raise serializers.ValidationError("Email and password are required")
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username' , 'email' , 'phone_number' ]

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=15 , required=True , write_only = True)   
    new_password = serializers.CharField(max_length=15 , required=True , write_only = True)   
    confirm_password = serializers.CharField(max_length=15 , required=True , write_only = True)  

    def validate(self, attrs):
        user = self.context.get('user')
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('your old password is not coorect')
        if attrs['new_password'] !=  attrs['confirm_password']:
            raise serializers.ValidationError('your new password is not match with confirm password')
        user.save()
        return attrs

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)   

    #validate otp
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        
        if user.is_active:
            raise serializers.ValidationError("User is already active")
        if user.otp != data['otp']:
            raise serializers.ValidationError("Invalid OTP")
        
        if user.otp_expires_at is None:
            raise serializers.ValidationError("OTP has no expiry time. Request a new one.")

        if user.otp_expires_at is None or timezone.now() > user.otp_expires_at:
            raise serializers.ValidationError("OTP has expired or is invalid. Request a new one.")  
        
        data['user'] = user
        return data  

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=15 , required=True , write_only = True)  
    new_password = serializers.CharField(max_length=15 , required=True , write_only = True)   
    confirm_password = serializers.CharField(max_length=15 , required=True , write_only = True)

    def validate(self, attrs):
        user = self.context.get('user')
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('your old password is not coorect')
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('your new password is not match with confirm password')
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Provide the refresh token.")

    def save(self, **kwargs):
        try:
            refresh_token = self.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError("Invalid or expired token.")
       
  