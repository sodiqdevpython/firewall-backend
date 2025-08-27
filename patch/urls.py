from django.urls import path
from .views import PatchManagementListCreateAPIView, PatchManagementDetailAPIView

urlpatterns = [
    path("patches/", PatchManagementListCreateAPIView.as_view(), name="patch-list-create"),
    path("patches/<int:pk>/", PatchManagementDetailAPIView.as_view(), name="patch-detail"),
]
