from rest_framework import serializers
from applications.models import Application
from hosts.serializers import DeviceNestedSerializer
from .models import FirewallRule
from applications.serializers import ApplicationSerializer


class FirewallRuleSerializer(serializers.ModelSerializer):
    host = DeviceNestedSerializer(read_only=True)
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = FirewallRule
        fields = ("id", "host", "application", "description", "title",
                  "port", "protocol", "direction", "action")
