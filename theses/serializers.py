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

# serializers.py
# class ThesisSerializer(serializers.ModelSerializer):
#     download_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Thesis
#         fields = '__all__'  # ou fais une liste explicite
#         # fields = ['id', 'title', 'resume', 'file', ... 'download_url']
#
#     def get_download_url(self, obj):
#         request = self.context.get('request')
#         return request.build_absolute_uri(f'/api/thesis/download/{obj.id}/')
