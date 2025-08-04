from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    NotificationPreferenceView,
    ProfileDetailView,
    ChangePasswordView,
    UpdateProfileView,
    AccountActivationView,
)

urlpatterns = [
    path('auth/activate/', AccountActivationView.as_view(), name='account-activate'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileDetailView.as_view(), name='profile'),
    path('auth/profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('notifications/preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
]