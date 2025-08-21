from rest_framework import serializers
from .models import FirewallRule, RuleAssignment


class FirewallRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirewallRule
        fields = '__all__'


class RuleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleAssignment
        fields = '__all__'
