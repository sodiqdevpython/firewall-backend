from rest_framework import serializers
from applications.models import Application
from hosts.serializers import DeviceNestedSerializer
from .models import FirewallRule, RuleAssignment
from applications.serializers import ApplicationSerializer


class FirewallRuleSerializer(serializers.ModelSerializer):
    application_hash = serializers.CharField(write_only=True)
    host = DeviceNestedSerializer(read_only=True)
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = FirewallRule
        fields = ("id", "host", "application_hash", "application",
                  "port", "protocol", "direction", "action")

    def create(self, validated_data):
        app_hash = validated_data.pop("application_hash", None)
        try:
            application = Application.objects.filter(hash=app_hash).first()
            # device = device  # Just to avoid unused variable warning
        except Application.DoesNotExist:
            raise serializers.ValidationError(
                {'application_hash': 'Invalid application hash'})
        validated_data['application'] = application
        return super().create(validated_data)


class RuleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleAssignment
        fields = '__all__'
