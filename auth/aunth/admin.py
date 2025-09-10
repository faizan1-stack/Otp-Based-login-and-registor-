from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id' , 'email' , 'username' , 'phone_number' )
    list_filter = ('email' , 'username', 'is_active')


