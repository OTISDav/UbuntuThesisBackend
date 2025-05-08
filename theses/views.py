from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Thesis, Favorite, Annotation
from .serializers import ThesisSerializer, FavoriteSerializer, AnnotationSerializer
from celery import shared_task
from rest_framework.permissions import IsAuthenticated


class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['field_of_study', 'year']
    search_fields = ['title', 'author', 'summary']
    ordering_fields = ['created_at', 'year']


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

# tâches Celery

from django.http import FileResponse, Http404
from rest_framework.views import APIView
from .models import Thesis
import os
from django.conf import settings

class MemoireDownloadView(APIView):
    def get(self, request, pk):
        try:
            thesis = Thesis.objects.get(pk=pk)
            file_path = thesis.document.path
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{thesis.title}.pdf"'
                return response
            else:
                raise Http404("Fichier non trouvé sur le serveur.")
        except Thesis.DoesNotExist:
            raise Http404("Mémoire non trouvé.")

    def post(self, request, pk):
        try:
            thesis = Thesis.objects.get(pk=pk)
            # Logique pour enregistrer le téléchargement (peut-être un modèle DownloadLog)
            # Pour l'instant, on se contente d'un print
            print(f"Téléchargement enregistré pour le mémoire ID: {thesis.id}, Titre: {thesis.title}, Utilisateur (non implémenté ici)")
            return Response({'message': 'Téléchargement enregistré avec succès.'}, status=200)
        except Thesis.DoesNotExist:
            return Response({'error': 'Mémoire non trouvé.'}, status=404)






