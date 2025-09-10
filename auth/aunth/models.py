from django.db import models
from django.contrib.auth.models import BaseUserManager ,AbstractBaseUser , PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None , password2=None):
        if not email:
           raise ValueError('Email is required')
    
        email = self.normalize_email(email)
        user = self.model(
           email=email,
           username=username,
           phone_number=phone_number,
           is_staff = False,
           is_superuser=False,
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None):
        user = self.create_user(
           email=email,
           username=username,
           phone_number=phone_number,
           password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_email_verified = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # Basic fields  
    email = models.EmailField(max_length=255, unique=True , null=False , blank=False)
    username = models.CharField(max_length=255 , unique=True , null=False , blank=False)
    phone_number = models.CharField(max_length=20 , unique=True , null=False , blank=False)
    # Additional fields
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    #OTP fields
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    max_otp_attempts = models.IntegerField(default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email