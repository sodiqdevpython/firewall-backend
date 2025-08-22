from rest_framework import viewsets
from .models import Application, Connection
from .serializers import ApplicationSerializer, ConnectionSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_fields = ['status', 'host', 'pid', 'hash']
    search_fields = ['name', 'hash', 'image_path']
    ordering_fields = ['name', 'pid', 'status']


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filterset_fields = ['application']
    search_fields = ['local_address', 'remote_address']
    ordering_fields = ['local_address', 'remote_address']