from django.http import FileResponse, Http404
from django.views import View
import os
from django.conf import settings

class DownloadDocumentView(View):
    def get(self, request, filename):
        filepath = os.path.join(settings.MEDIA_ROOT, 'documents', filename)
        if os.path.exists(filepath):
            try:
                return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier : {e}")
                raise Http404("Erreur lors du téléchargement du fichier")
        raise Http404("Fichier non trouvé")