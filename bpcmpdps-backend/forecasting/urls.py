from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ForecastViewSet

router = DefaultRouter()
router.register(r"", ForecastViewSet, basename="forecasting")

urlpatterns = [
    path("", include(router.urls)),
]