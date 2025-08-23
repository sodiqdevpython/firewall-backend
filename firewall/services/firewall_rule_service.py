from django.core.exceptions import ValidationError
from django.db import transaction
from applications.models import Application
from hosts.models import Device
from firewall.models import FirewallRule


class FirewallRuleService:
    @staticmethod
    @transaction.atomic
    def create_firewall_rule(data):
        host_bios_uuid = data.pop('host', None)
        application_hash = data.pop('application_hash', None)

        if not host_bios_uuid:
            raise ValidationError("Host BIOS UUID is required.")
        if not application_hash:
            raise ValidationError("Application hash is required.")

        try:
            device = Device.objects.get(bios_uuid=host_bios_uuid)
        except Device.DoesNotExist:
            raise ValidationError("Device with the given BIOS UUID does not exist.")

        try:
            application = Application.objects.get(hash=application_hash)
        except Application.DoesNotExist:
            raise ValidationError("Application with the given hash does not exist.")

        firewall_rule = FirewallRule.objects.create(
            host=device,
            application=application,
            **data
        )
        return firewall_rule


