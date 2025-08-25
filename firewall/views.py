from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import FirewallRule
from .serializers import FirewallRuleSerializer
from hosts.models import Device
from applications.models import Application
import json
from django.core.serializers.json import DjangoJSONEncoder


class FirewallRuleViewSet(viewsets.ModelViewSet):
    queryset = FirewallRule.objects.all()
    serializer_class = FirewallRuleSerializer
    filterset_fields = ['host', 'application', 'protocol', 'direction', 'action', 'port']
    search_fields = ['protocol', 'direction', 'action']
    ordering_fields = ['port', 'protocol', 'direction']

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        host_data = data.pop("host", None)  # host ni olib tashlaymiz

        if isinstance(host_data, dict):
            host_name = host_data.get("host_name")
            try:
                device = Device.objects.get(host_name=host_name)
            except Device.DoesNotExist:
                raise ValidationError("Device with the given host_name does not exist.")
        else:
            try:
                device = Device.objects.get(bios_uuid=host_data)
            except Device.DoesNotExist:
                raise ValidationError("Device with the given BIOS UUID does not exist.")

        firewall_rule = FirewallRule.objects.create(
            host=device,
            **data  # endi host yo‘q
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"device_{firewall_rule.host.bios_uuid}",
            {
                "type": "firewall.rule",
                "event": "created",
                "rule": json.loads(json.dumps(FirewallRuleSerializer(firewall_rule).data, cls=DjangoJSONEncoder)),
            }
        )

        serializer = self.get_serializer(firewall_rule)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        rule_data = json.loads(json.dumps(self.get_serializer(instance).data, cls=DjangoJSONEncoder))
        bios_uuid = instance.host.bios_uuid

        self.perform_destroy(instance)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"device_{bios_uuid}",
            {
                "type": "firewall.rule",
                "event": "deleted",
                "rule": rule_data,
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
