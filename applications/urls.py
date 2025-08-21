from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ApplicationViewSet, ConnectionViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'connections', ConnectionViewSet, basename='connection')

urlpatterns = [
    path('', include(router.urls)),
]
