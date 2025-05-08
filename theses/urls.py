from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ThesisViewSet,
    FavoriteViewSet,
    AnnotationViewSet,
    SuggestionsView,
)

router = DefaultRouter()
router.register(r'theses', ThesisViewSet, basename='thesis')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'annotations', AnnotationViewSet, basename='annotation')

urlpatterns = [
    path('', include(router.urls)),
    path('suggestions/', SuggestionsView.as_view({'get': 'list'}), name='suggestions'),
    # ✅ Ajoutez explicitement la route pour le téléchargement
    path('memoire/download/<int:pk>/', MemoireDownloadView.as_view(), name='memoire-download'),
]
