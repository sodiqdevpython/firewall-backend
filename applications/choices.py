from django.db.models import TextChoices


class ApplicationStatusChoice(TextChoices):
    Running = "running"
    Stopped = "stopped"


class ConnectionDirectionChoice(TextChoices):
    INBOUND = "Inbound", "Inbound"
    OUTBOUND = "Outbound", "Outbound"