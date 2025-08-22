from django.db.models import TextChoices

class ApplicationStatusChoice(TextChoices):
    Running = "running"
    Stopped = "stopped"
