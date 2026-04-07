from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DemandForecast
from .services import run_demand_forecast
from django.utils import timezone


class DemandForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandForecast
        fields = [
            "id",
            "prediction_made_at",
            "target_time",
            "horizon_steps",
            "predicted_demand_kw",
            "model_version",
        ]


class ForecastViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DemandForecast.objects.order_by("-target_time")
    serializer_class = DemandForecastSerializer

    @action(detail=False, methods=["post"])
    def run_now(self, request):
        saved = run_demand_forecast()
        data = DemandForecastSerializer(saved, many=True).data
        return Response(
            {
                "detail": "Demand forecast run completed.",
                "count": len(saved),
                "results": data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def latest(self, request):
        # REAL-TIME MODE (keep for future live deployment)
        now = timezone.now()
        qs = DemandForecast.objects.filter(
            target_time__gte=now,
            horizon_steps=12,
        ).order_by("target_time")[:60]

        # TESTING MODE (2025 simulated future)
        # latest_record = DemandForecast.objects.order_by("-target_time").first()
        # if latest_record is None:
        #     return Response([])

        # now = latest_record.target_time
        # qs = DemandForecast.objects.filter(target_time__gte=now).order_by("target_time")[:13]

        return Response(DemandForecastSerializer(qs, many=True).data)