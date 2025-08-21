from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def broadcast(groups: list[str], event_type: str, data: dict):
    """
    groups: ["applications", "host_<uuid>", ...]
    event_type: channels handler nomi (mas: "app_created")
    data: JSON-serializable payload
    """
    channel_layer = get_channel_layer()
    for group in groups:
        async_to_sync(channel_layer.group_send)(
            group,
            {"type": event_type, "data": data}
        )
