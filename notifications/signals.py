from django.db.models.signals import post_save
from django.dispatch import receiver
from theses.models import Thesis, SavedSearch
from .models import Notification
from .utils import send_push_notification

@receiver(post_save, sender=Thesis)
def notify_users_new_thesis(sender, instance, created, **kwargs):
    if created:
        searches = SavedSearch.objects.all()
        for search in searches:
            params = search.query_params or {}

            matches_field = (params.get('field_of_study') in (None, instance.field_of_study))
            matches_year = (params.get('year') in (None, str(instance.year)))

            if matches_field and matches_year:
                Notification.objects.create(
                    user=search.user,
                    message=f"Nouveau document publié: '{instance.title}'"
                )
                send_push_notification(
                    user=search.user,
                    title="Nouveau document disponible",
                    message=f"Le document '{instance.title}' correspond à votre recherche."
                )
