from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static
from users.views import reset_password_page  # ta vue qui rend le template



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
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('reset-password/', reset_password_page, name='reset_password_page'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/users/', include('users.urls')),
    path('api/theses/', include('theses.urls')),
    path('documents/', include('documents.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)