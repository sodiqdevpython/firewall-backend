from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ApplicationViewSet, ConnectionViewSet, ConnectionRemoteAPIView, ConnectionListAPIView

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'connections', ConnectionViewSet, basename='connection')

urlpatterns = [
    path('', include(router.urls)),
    path("remote/", ConnectionRemoteAPIView.as_view(), name="connections-remote"),
    path("connect/list/", ConnectionListAPIView.as_view(), name="connection-list"),
]
