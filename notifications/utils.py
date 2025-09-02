from fcm_django.models import FCMDevice

def send_push_notification(user, title, message):
    devices = FCMDevice.objects.filter(user=user, active=True)
    devices.send_message(message, title=title)
