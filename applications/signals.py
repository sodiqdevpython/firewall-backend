from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.realtime import broadcast
from .models import Application, Connection

def _safe_dt(dt):
    return dt.isoformat() if dt else None

@receiver(post_save, sender=Application)
def application_created(sender, instance: Application, created, **kwargs):
    if not created:
        return
    host_id = str(instance.host_id) if instance.host_id else None
    data = {
        "event": "application.created",
        "application": {
            "id": str(instance.id),
            "host_id": host_id,
            "image_path": instance.image_path,
            "pid": instance.pid,
            "name": instance.name,
            "hash": instance.hash,
            "status": instance.status,
            "created_at": _safe_dt(instance.created_at),
        }
    }
    groups = ["applications"]
    if host_id:
        groups.append(f"host_{host_id}")
    broadcast(groups, "app_created", data)

@receiver(post_save, sender=Connection)
def connection_created(sender, instance: Connection, created, **kwargs):
    if not created:
        return
    app = instance.application
    host_id = str(app.host_id) if app and app.host_id else None
    data = {
        "event": "connection.created",
        "connection": {
            "id": str(instance.id),
            "application_id": str(app.id) if app else None,
            "host_id": host_id,
            "protocol": instance.protocol,
            "local_address": instance.local_address,
            "remote_address": instance.remote_address,
            "more_info": instance.more_info or None,
            "created_at": _safe_dt(instance.created_at),
        }
    }
    groups = ["connections"]
    if host_id:
        groups.append(f"host_{host_id}")
    broadcast(groups, "connection_created", data)
