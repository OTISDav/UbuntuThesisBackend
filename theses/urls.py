from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ThesisViewSet,
    FavoriteViewSet,
    AnnotationViewSet,
    SuggestionsView,
    ThesisDownloadView,
    SavedSearchViewSet,
)

router = DefaultRouter()
router.register(r'theses', ThesisViewSet, basename='thesis')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'annotations', AnnotationViewSet, basename='annotation')
router.register(r'saved-searches', SavedSearchViewSet, basename='savedsearch')


urlpatterns = [
    path('', include(router.urls)),
    path('download/<int:pk>/', ThesisDownloadView.as_view(), name='thesis-download'),
    path('suggestions/', SuggestionsView.as_view({'get': 'list'}), name='suggestions'),
    # ✅ Ajoutez explicitement la route pour le téléchargement
]
