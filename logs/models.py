from django.db import models

from .choices import AgentLogChoice
from utils.models import BaseModel


class AgentLog(BaseModel):
    host = models.ForeignKey('hosts.Device', on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=AgentLogChoice.choices, default=AgentLogChoice.INFO)
    message = models.TextField()

    def __str__(self):
        return f"{self.host} {self.level}"
