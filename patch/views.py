from rest_framework import generics
from .models import PatchManagement
from .serializers import PatchManagementSerializer


class PatchManagementListCreateAPIView(generics.ListCreateAPIView):
    queryset = PatchManagement.objects.all().select_related("device")
    serializer_class = PatchManagementSerializer


class PatchManagementDetailAPIView(generics.RetrieveAPIView):
    queryset = PatchManagement.objects.all().select_related("device")
    serializer_class = PatchManagementSerializer


class PatchManagementUpdateAPIView(generics.UpdateAPIView):
    queryset = PatchManagement.objects.all()
    serializer_class = PatchManagementSerializer
