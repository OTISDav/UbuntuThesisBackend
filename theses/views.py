from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Thesis, Favorite, Annotation
from .serializers import ThesisSerializer, FavoriteSerializer, AnnotationSerializer
from celery import shared_task
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from cloudinary.uploader import upload
import os



class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['field_of_study', 'year']
    search_fields = ['title', 'author', 'summary']
    ordering_fields = ['created_at', 'year']

    def perform_create(self, serializer):
        document = self.request.FILES.get("document")  # correspond à la clé dans Flutter

        if not document:
            raise ValidationError({"document": "Aucun fichier PDF reçu."})

        # Upload Cloudinary
        result = upload(document, resource_type="raw", folder="documents/")
        file_url = result.get("secure_url")

        if not file_url:
            raise ValidationError({"file": "Échec de l'envoi à Cloudinary."})

        # Sauvegarde avec l’URL Cloudinary
        serializer.save(author=self.request.user, file=file_url)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)  # ✅ Retourne uniquement les favoris de l'utilisateur

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # ✅ Ajoute `user` automatiquement

    @action(detail=False, methods=['get'])
    def user_favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_favorite(self, request, pk=None):
        user = request.user
        try:
            favorite = Favorite.objects.get(user=user, thesis_id=pk)  # ✅ Supprime par `thesis_id`
            favorite.delete()
            return Response({'message': 'Favorite removed successfully'})
        except Favorite.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=404)

class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Annotation.objects.filter(user=self.request.user)  # ✅ Seules les annotations de l'utilisateur connecté

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # ✅ Ajoute automatiquement `user`

    @action(detail=False, methods=['get'])
    def user_annotations(self, request):
        annotations = Annotation.objects.filter(user=request.user)
        serializer = self.get_serializer(annotations, many=True)
        parser_classes = [MultiPartParser]
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_annotation(self, request, pk=None):
        user = request.user
        try:
            annotation = Annotation.objects.get(user=user, pk=pk)
            annotation.note = request.data.get('note', annotation.note)
            annotation.save()
            serializer = self.get_serializer(annotation)
            return Response(serializer.data)
        except Annotation.DoesNotExist:
            return Response({'error': 'Annotation not found'}, status=404)


class SuggestionsView(viewsets.ViewSet):
    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user).values_list('thesis__field_of_study', flat=True)
        suggestions = Thesis.objects.filter(field_of_study__in=favorites).exclude(favorite__user=user)[:5]
        serializer = ThesisSerializer(suggestions, many=True)
        return Response(serializer.data)

class ThesisDownloadView(APIView):
    permission_classes = [IsAuthenticated]  # Facultatif si accès restreint

    def get(self, request, pk):
        try:
            thesis = Thesis.objects.get(pk=pk)
            file_path = thesis.file.path
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            else:
                raise Http404("Fichier non trouvé.")
        except Thesis.DoesNotExist:
            raise Http404("Thèse non trouvée.")
