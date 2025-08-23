from django.db.models import TextChoices


class AgentLogChoice(TextChoices):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
