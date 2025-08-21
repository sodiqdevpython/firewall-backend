from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DeviceViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')

urlpatterns = [
    path('', include(router.urls)),
]
