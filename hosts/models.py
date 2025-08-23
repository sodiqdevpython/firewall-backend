from django.db import models
from utils.models import BaseModel
from .choices import DeviceStatusChoice


class Device(BaseModel):
    bios_uuid = models.UUIDField(unique=True)
    host_name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    status = models.CharField(choices=DeviceStatusChoice.choices, default=DeviceStatusChoice.Offline, max_length=24)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.host_name
