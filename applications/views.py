from rest_framework import viewsets, generics, views
from .models import Application, Connection
from .serializers import ApplicationSerializer, ConnectionSerializer
from hosts.models import Device
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
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
    filterset_fields = ['application__host__bios_uuid', ]
    search_fields = ['local_address', 'remote_address']
    ordering_fields = ['local_address', 'remote_address']


class ConnectionRemoteAPIView(views.APIView):
    def get(self, request):
        latest = (
            Connection.objects
            .filter(remote_address=OuterRef("remote_address"))
            .order_by("-created_at")
        )

        connections = (
            Connection.objects
            .filter(id=Subquery(latest.values("id")[:1]))
            .values_list("remote_address", flat=True)
        )

        return Response(list(connections))


class ConnectionListAPIView(generics.ListAPIView):
    serializer_class = ConnectionSerializer
    filterset_fields = ['application__host__bios_uuid', ]

    def get_queryset(self):
        latest = Connection.objects.filter(remote_address=OuterRef("remote_address")).order_by("-created_at")
        connections = Connection.objects.filter(id=Subquery(latest.values("id")[:1]))
        return connections
