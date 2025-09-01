from rest_framework.routers import DefaultRouter
from .views import FCMDeviceViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'fcm-devices', FCMDeviceViewSet, basename='fcm-device')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls
