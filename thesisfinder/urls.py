from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="ThesisFinder API",
        default_version='v1',
        description="API documentation for ThesisFinder",
        contact=openapi.Contact(email="contact@thesisfinder.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('api/auth/', include('dj_rest_auth.urls')),
    path('api/users/', include('users.urls')),
    path('api/theses/', include('theses.urls')),
    path('documents/', include('documents.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)