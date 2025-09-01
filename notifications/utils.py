from push_notifications.models import GCMDevice


def send_push_notification(user, title, message):
    devices = GCMDevice.objects.filter(user=user, active=True)
    devices.send_message(title=title, body=message)
