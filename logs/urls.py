from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AgentLogViewSet

router = DefaultRouter()
router.register(r'agent-logs', AgentLogViewSet, basename='agentlog')

urlpatterns = [
    path('', include(router.urls)),
]
