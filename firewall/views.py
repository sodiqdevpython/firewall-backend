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

        firewall_rule = FirewallRule.objects.create(
            **{k: v for k, v in data.items()}
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all_devices",
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

        self.perform_destroy(instance)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"all_devices",
            {
                "type": "firewall.rule",
                "event": "deleted",
                "rule": rule_data,
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
