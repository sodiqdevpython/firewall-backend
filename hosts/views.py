from rest_framework import viewsets
from .serializers import DeviceSerializer
from .models import Device


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_fields = ['status', 'os_version', 'ip_address', 'bios_uuid']
    search_fields = ['host_name', 'ip_address', 'bios_uuid']
    ordering_fields = ['last_seen', 'host_name', 'ip_address']
