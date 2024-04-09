# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Product

@receiver(post_save, sender=Product)
def notify_clients_on_save(sender, instance, created, **kwargs):
    if created:
        action = 'create'
    else:
        action = 'update'
    send_websocket_message(action, instance.pk)

@receiver(post_delete, sender=Product)
def notify_clients_on_delete(sender, instance, **kwargs):
    send_websocket_message('delete', instance.pk)

def send_websocket_message(action, pk):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_group",
        {
            "type": "notification",
            "action": action,
            "pk": pk,
        }
    )
