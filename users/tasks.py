from celery import shared_task
from django.core.mail import send_mail
from .models import NotificationPreference
from theses.models import Thesis

@shared_task
def notify_users_on_new_thesis(thesis_id):
    thesis = Thesis.objects.get(id=thesis_id)
    users = NotificationPreference.objects.filter(notify_on_new_theses=True).values_list('user__email', flat=True)

    for email in users:
        send_mail(
            subject="Nouvelle thèse disponible",
            message=f"Une nouvelle thèse '{thesis.title}' est disponible. Consultez-la maintenant !",
            from_email="noreply@thesisfinder.com",
            recipient_list=[email],
        )
