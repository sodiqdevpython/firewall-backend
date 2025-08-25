from django.db import models

from .choices import ApplicationStatusChoice, ConnectionDirectionChoice
from utils.models import BaseModel


class Application(BaseModel):
    host = models.ForeignKey("hosts.Device", on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    pid = models.PositiveIntegerField()
    name = models.CharField(max_length=1024)
    sent = models.CharField(max_length=256, null=True, blank=True)
    received = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class Connection(BaseModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True, blank=True)
    direction = models.CharField(max_length=20, choices=ConnectionDirectionChoice.choices)
    local_address = models.CharField(max_length=128)
    remote_address = models.CharField(max_length=128)
    bytes = models.PositiveIntegerField()
    more_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.local_address} -> {self.remote_address}"
