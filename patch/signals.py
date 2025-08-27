from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import PatchManagement


@receiver(post_save, sender=PatchManagement)
def patchmanagement_signal(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    group_name = f"device_{instance.device.bios_uuid}"

    if instance.download_patch:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "download_patch",
                "data": {
                    "id": instance.id,
                    "title": instance.title,
                    "kb": instance.kb,
                    "support": instance.support
                }
            }
        )

    if instance.install_patch:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "install_patch",
                "data": {
                    "id": instance.id,
                    "title": instance.title,
                    "kb": instance.kb,
                    "support": instance.support
                }
            }
        )
