from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone_number')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_staff', 'is_active')



admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
