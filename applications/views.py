from rest_framework import viewsets, generics
from .models import Application, Connection
from .serializers import ApplicationSerializer, ConnectionSerializer
from hosts.models import Device
from rest_framework.response import Response
from rest_framework import status


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_fields = ['host', 'pid']
    search_fields = ['name', 'image_path']
    ordering_fields = ['name', 'pid']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filterset_fields = ['application__host__bios_uuid',]
    search_fields = ['local_address', 'remote_address']
    ordering_fields = ['local_address', 'remote_address']
