from django.db import models

from .choices import ApplicationStatusChoice, ConnectionProtocolChoice, ConnectionDirectionChoice, ConnectionStatusChoice
from utils.models import BaseModel

class Application(BaseModel):
    host = models.ForeignKey("hosts.Device", on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    pid = models.PositiveIntegerField()
    name = models.CharField(max_length=1024)
    hash = models.CharField(max_length=64)
    status = models.CharField(max_length=10, choices=ApplicationStatusChoice.choices,default=ApplicationStatusChoice.Running)

    def __str__(self):
        return self.name

class Connection(BaseModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=10, choices=ConnectionProtocolChoice.choices)
    direction = models.CharField(max_length=10, choices=ConnectionDirectionChoice.choices)
    local_address = models.CharField(max_length=128)
    remote_address = models.CharField(max_length=128)
    status = models.CharField(max_length=10, choices=ConnectionStatusChoice.choices)
    more_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.remote_address