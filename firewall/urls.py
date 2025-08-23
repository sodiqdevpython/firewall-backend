from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FirewallRuleViewSet

router = DefaultRouter()
router.register(r'firewall-rules', FirewallRuleViewSet, basename='firewallrule')

urlpatterns = [
    path('', include(router.urls)),
]
