# import jwt
# import datetime
# from django.conf import settings
# from django.core.mail import send_mail
# from django.utils import timezone
# #
# def send_verification_email(user, frontend_url):
#     payload = {
#         'user_id': user.id,
#         'exp': (timezone.now() + datetime.timedelta(hours=24)).timestamp(),
#         'type': 'email_verification'
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#
#     activation_link = f"{frontend_url}/activate/?token={token}"
#
#     ici = {activation_link}
#     subject = 'Activez votre compte'
#     message = f"""
#     Bonjour {user.username},
#
#     Merci de vous être inscrit. Veuillez cliquer sur le lien ci-dessous pour activer votre compte :
#
#     # {activation_link}
#
#         <p>
#             <a href="{activation_link}" style="padding: 10px 15px; background-color: #00A8AA; color: white; text-decoration: none; border-radius: 5px;">
#                 Cliquez ici pour activer votre compte
#             </a>
#         </p>
#
#     Ce lien expirera dans 24 heures.
#
#     Si vous n'avez pas demandé ce compte, ignorez cet email.
#
#     Cordialement,
#     L'équipe de votre application.
#     """
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#     )

import jwt
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django_rest_passwordreset.signals import reset_password_token_created


def send_verification_email(user, frontend_url):
    payload = {
        'user_id': user.id,
        'exp': (timezone.now() + datetime.timedelta(hours=24)).timestamp(),
        'type': 'email_verification'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # Si le token est en bytes (selon version), le décoder
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    activation_link = f"{frontend_url}/activate/?token={token}"

    subject = 'Activez votre compte'
    text_content = f"Bonjour {user.username},\nVeuillez activer votre compte en cliquant sur le lien envoyé."
    html_content = f"""
        <p>Bonjour {user.username},</p>
        <p>Merci de vous être inscrit.</p>
        <p>
            <a href="{activation_link}" style="padding: 10px 15px; background-color: #00A8AA; color: white; text-decoration: none; border-radius: 5px;">
                Cliquez ici pour activer votre compte
            </a>
        </p>
        <p>Ce lien expirera dans 24 heures.</p>
        <p>Si vous n'avez pas demandé ce compte, ignorez cet email.</p>
        <p>Cordialement,<br>L'équipe de votre application.</p>
    """

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

from django.dispatch import receiver

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    user = reset_password_token.user
    token = reset_password_token.key

    frontend_url = "https://ubuntuthesisbackend.onrender.com/api/users"  # 🔁 change avec ton vrai URL front


    reset_link = f"{frontend_url}/reset-password/?token={token}"

    subject = "Réinitialisation de votre mot de passe"
    text_content = f"Bonjour {user.username},\nPour réinitialiser votre mot de passe, cliquez sur ce lien : {reset_link}"
    html_content = f"""
        <p>Bonjour {user.username},</p>
        <p>Vous avez demandé la réinitialisation de votre mot de passe.</p>
        <p>
            <a href="{reset_link}" style="padding:10px 15px; background:#00A8AA; color:#fff; text-decoration:none; border-radius:5px;">
                Réinitialiser mon mot de passe
            </a>
        </p>
        <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.</p>
        <p>Cordialement,<br>L'équipe de votre application.</p>
    """

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()