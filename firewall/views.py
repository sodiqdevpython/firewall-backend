from rest_framework import viewsets
from .models import FirewallRule, RuleAssignment
from .serializers import FirewallRuleSerializer, RuleAssignmentSerializer


class FirewallRuleViewSet(viewsets.ModelViewSet):
    queryset = FirewallRule.objects.all()
    serializer_class = FirewallRuleSerializer
    filterset_fields = ['host', 'application', 'protocol', 'direction', 'action', 'port']
    search_fields = ['protocol', 'direction', 'action']
    ordering_fields = ['port', 'protocol', 'direction']


class RuleAssignmentViewSet(viewsets.ModelViewSet):
    queryset = RuleAssignment.objects.all()
    serializer_class = RuleAssignmentSerializer
    filterset_fields = ['status', 'rule', 'host']
    search_fields = ['rule__protocol', 'rule__direction', 'host__host_name']
    ordering_fields = ['status', 'rule', 'host']