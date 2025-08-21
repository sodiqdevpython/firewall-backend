from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.realtime import broadcast
from .models import AgentLog

def _safe_dt(dt):
    return dt.isoformat() if dt else None

@receiver(post_save, sender=AgentLog)
def agentlog_created(sender, instance: AgentLog, created, **kwargs):
    if not created:
        return
    host_id = str(instance.host_id) if instance.host_id else None
    data = {
        "event": "agentlog.created",
        "log": {
            "id": str(instance.id),
            "host_id": host_id,
            "level": instance.level,
            "message": instance.message,
            "created_at": _safe_dt(instance.created_at),
        }
    }
    groups = ["agentlogs"]
    if host_id:
        groups.append(f"host_{host_id}")
    broadcast(groups, "agentlog_created", data)
