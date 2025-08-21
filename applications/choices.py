from django.db.models import TextChoices

class ApplicationStatusChoice(TextChoices):
    Running = "running"
    Stopped = "stopped"

class ConnectionProtocolChoice(TextChoices):
    TCP = "tcp"
    UDP = "udp"

class ConnectionDirectionChoice(TextChoices):
    IN = "inbound"
    OUT = "outbound"

class ConnectionStatusChoice(TextChoices):
    Allowed = "allowed"
    Blocked = "blocked"