from django.db import models

class DeviceStatusChoice(models.TextChoices):
    Online = "Online"
    Offline = "Offline"