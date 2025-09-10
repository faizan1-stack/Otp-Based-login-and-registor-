from django import forms
from .models import *

class FormView(forms.ModelForm):
    class Meta:
        model = CustomUserManager
        fields = '__all__'

    def user(self, request , cleaned_data):
        user = CustomUserManager.objects.get(
            email = cleaned_data.get("email"),
            username = cleaned_data.get("username"),
            phone_number= cleaned_data.get("phone_number"),
            password = cleaned_data.get("password"),
        )
        return user