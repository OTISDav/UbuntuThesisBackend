from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt


from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    NotificationPreferenceView,
    ProfileDetailView,
    ChangePasswordView,
    UpdateProfileView,
    AccountActivationView,
    CsrfExemptResetPasswordRequestToken,
    CsrfExemptResetPasswordConfirm
)


urlpatterns = [
    path('password_reset/', CsrfExemptResetPasswordRequestToken.as_view(), name='password_reset'),
    path('password_reset/confirm/', CsrfExemptResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('auth/activate/', AccountActivationView.as_view(), name='account-activate'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileDetailView.as_view(), name='profile'),
    path('auth/profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('notifications/preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
]