from rest_framework import serializers
from push_notifications.models import GCMDevice
from .models import Notification

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
        fields = ['registration_id', 'type', 'user']
        extra_kwargs = {'user': {'read_only': True}}

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
