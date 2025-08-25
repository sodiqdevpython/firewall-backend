from celery import shared_task
from .models import Connection
from .utils import ip_lookup_online  # sizning ip_lookup_online functioningiz

@shared_task
def fetch_more_info(connection_id, remote_ip):
    try:
        connection = Connection.objects.get(id=connection_id)
        connection.more_info = {
            "remote_address": ip_lookup_online(remote_ip)
        }
        connection.save(update_fields=["more_info"])
    except Connection.DoesNotExist:
        pass
