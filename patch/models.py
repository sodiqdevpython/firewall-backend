from django.db import models
from utils.models import BaseModel
from hosts.models import Device

nb = dict(null=True, blank=True)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class PatchManagement(BaseModel):
    title = models.CharField(max_length=512)
    support = models.CharField(max_length=521)
    kb = models.CharField(max_length=521)
    update_id = models.CharField(max_length=521, **nb)

    mandatory = models.BooleanField(default=False)
    reboot_required = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    download_patch = models.BooleanField(default=False)
    install_patch = models.BooleanField(default=False)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        channel_layer = get_channel_layer()
        group_name = f"device_{str(self.device.bios_uuid)}"

        # ⚡ ustuvorlik: install > download
        if self.install_patch:
            event_type = "install_patch"
        elif self.download_patch:
            event_type = "download_patch"
        else:
            event_type = None

        if event_type:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": event_type,
                    "data": {
                        "id": str(self.id),
                        "title": self.title,
                        "kb": self.kb,
                        "support": self.support,
                        "update_id": self.update_id,
                        "device_bios_uuid": str(self.device.bios_uuid),
                    },
                },
            )
