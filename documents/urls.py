from django.urls import path
from . import views

urlpatterns = [
    # Route pour télécharger un fichier par son nom (correspond à l'URL que vous avez)
    path('<str:filename>.pdf/', views.DownloadDocumentView.as_view(), name='download-document-by-name'),
    # Vous pouvez ajouter d'autres routes ici si nécessaire, par exemple pour télécharger par ID
    # path('download/<int:document_id>/', views.DownloadDocumentView.as_view(), name='download-document-by-id'),
]