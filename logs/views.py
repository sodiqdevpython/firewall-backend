from rest_framework import viewsets
from .models import AgentLog
from .serializers import AgentLogSerializer


class AgentLogViewSet(viewsets.ModelViewSet):
    queryset = AgentLog.objects.all()
    serializer_class = AgentLogSerializer
    filterset_fields = ['level', 'host']
    search_fields = ['message', 'host__host_name']
    ordering_fields = ['timestamp', 'level']