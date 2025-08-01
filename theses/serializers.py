from .models import Thesis, Favorite, Annotation
from rest_framework import serializers

class ThesisSerializer(serializers.ModelSerializer):
    file = serializers.URLField(required=False)

    class Meta:
        model = Thesis
        fields = '__all__'

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

# serializers.py
class ThesisSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Thesis
        fields = '__all__'  # ou fais une liste explicite
        # fields = ['id', 'title', 'resume', 'file', ... 'download_url']

    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/thesis/download/{obj.id}/')
