from rest_framework import viewsets, permissions
from push_notifications.models import GCMDevice
from .serializers import NotificationSerializer
from .models import Notification
from rest_framework import viewsets, permissions
from fcm_django.models import FCMDevice
from .serializers import FCMDeviceSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')




class FCMDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = FCMDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FCMDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
