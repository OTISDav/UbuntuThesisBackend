from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import NotificationPreference, Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_verified')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'email', 'profile_picture']

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = '__all__'
