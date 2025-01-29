from rest_framework import serializers
from .models import Thesis, Favorite, Annotation

class ThesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis
        fields = '__all__'

from rest_framework import serializers
from .models import Favorite, Annotation

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}  # 🔹 Ne pas exiger que l'utilisateur soit envoyé

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}  # 🔹 Ne pas exiger que l'utilisateur soit envoyé

