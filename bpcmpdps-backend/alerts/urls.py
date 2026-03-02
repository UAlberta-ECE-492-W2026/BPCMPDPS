from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ThresholdViewSet, AlertViewSet

router = DefaultRouter()
router.register(r"thresholds", ThresholdViewSet, basename="thresholds")
router.register(r"", AlertViewSet, basename="alerts")

urlpatterns = [
    path("", include(router.urls)),
]