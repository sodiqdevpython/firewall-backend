from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import FirewallRule, RuleAssignment
from .serializers import FirewallRuleSerializer, RuleAssignmentSerializer
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

        host_data = data.get("host")
        application_hash = data.get("application_hash")

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

        if not application_hash:
            raise ValidationError("Application hash is required.")

        try:
            application = Application.objects.filter(hash=application_hash).first()
        except Application.DoesNotExist:
            raise ValidationError("Application with the given hash does not exist.")

        firewall_rule = FirewallRule.objects.create(
            host=device,
            application=application,
            **{k: v for k, v in data.items() if k not in ["host", "application_hash"]}
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"device_{firewall_rule.host.bios_uuid}",
            {
                "type": "firewall.rule",
                "rule": json.loads(json.dumps(FirewallRuleSerializer(firewall_rule).data, cls=DjangoJSONEncoder)),
            }
        )

        serializer = self.get_serializer(firewall_rule)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RuleAssignmentViewSet(viewsets.ModelViewSet):
    queryset = RuleAssignment.objects.all()
    serializer_class = RuleAssignmentSerializer
    filterset_fields = ['status', 'rule', 'host']
    search_fields = ['rule__protocol', 'rule__direction', 'host__host_name']
    ordering_fields = ['status', 'rule', 'host']
