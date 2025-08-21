from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FirewallRuleViewSet, RuleAssignmentViewSet

router = DefaultRouter()
router.register(r'firewall-rules', FirewallRuleViewSet, basename='firewallrule')
router.register(r'rule-assignments', RuleAssignmentViewSet, basename='ruleassignment')

urlpatterns = [
    path('', include(router.urls)),
]
