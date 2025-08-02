from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile, NotificationPreference

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    ordering = ('id',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture_display')
    search_fields = ('user__username', 'user__email')

    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return "-"
    profile_picture_display.short_description = 'Photo de profil'

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'push_notifications', 'sms_notifications')
    search_fields = ('user__username', 'user__email')

