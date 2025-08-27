from django.db import models
from utils.models import BaseModel
from hosts.models import Device

nb = dict(null=True, blank=True)


class PatchManagement(BaseModel):
    title = models.CharField(max_length=512)
    support = models.CharField(max_length=521)
    kb = models.CharField(max_length=521)

    mandatory = models.BooleanField(default=False)
    reboot_required = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
