from .views import *
from django.urls import path

urlpatterns = [
   path('api/register' ,  RegisterView.as_view() , name = 'registor'),
   path('api/login' ,  LoginView.as_view() , name = 'login'),
   path('api/ResendOtp/', ProfileView.as_view() , name='profile'),
   path('api/ResetPassword/', ResetPasswordView.as_view() , name='reset_password'),
   path('api/verify-otp/', OtpView.as_view() , name='verify_otp'),
   path('api/resend-otp/', ResendOtpView.as_view() , name='resend_otp'),
   path('api/change-password/', ChangePasswordView.as_view() , name='change_password'),
   path('api/logout/', LogoutView.as_view() , name='logout'),
   path('api/user-profile/', ProfileView.as_view() , name='user_profile'),
]
