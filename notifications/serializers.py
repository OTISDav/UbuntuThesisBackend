from rest_framework import serializers
from push_notifications.models import GCMDevice
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']


from rest_framework import serializers
from fcm_django.models import FCMDevice

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ['id', 'registration_id', 'name', 'device_id', 'type', 'user']
        read_only_fields = ['user']

