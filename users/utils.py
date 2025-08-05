import jwt
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

def send_verification_email(user, frontend_url):
    payload = {
        'user_id': user.id,
        'exp': (timezone.now() + datetime.timedelta(hours=24)).timestamp(),
        'type': 'email_verification'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    activation_link = f"{frontend_url}/activate/?token={token}"

    subject = 'Activez votre compte'
    message = f"""
    Bonjour {user.username},

    Merci de vous être inscrit. Veuillez cliquer sur le lien ci-dessous pour activer votre compte :

    {activation_link}

    Ce lien expirera dans 24 heures.

    Si vous n'avez pas demandé ce compte, ignorez cet email.

    Cordialement,
    L'équipe de votre application.
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
