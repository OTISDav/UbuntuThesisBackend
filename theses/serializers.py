from .models import Thesis, Favorite, Annotation
from rest_framework import serializers

# class ThesisSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Thesis
#         fields = '__all__'

class ThesisSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    class Meta:
        model = Thesis
        fields = '__all__'

    # def get_document(self, obj):
    #     if obj.document:
    #         return obj.document.url  # ici on renvoie l'URL complète
    #     return None

    def get_document(self, obj):
        if obj.document:
            # Si c'est déjà une string, on la renvoie telle quelle
            if isinstance(obj.document, str):
                return obj.document
            # Sinon on retourne l'URL du fichier CloudinaryField
            return obj.document.url
        return None

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

from rest_framework import serializers
from .models import SavedSearch

class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = ['id', 'name', 'query_params', 'created_at', 'updated_at']
