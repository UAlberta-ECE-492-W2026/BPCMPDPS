from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .Model import DemandPrice
from .service import run_get_Price
from django.utils import timezone


class DemandPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandPrice
        fields = ["id", "prediction_time","target_time","horizon_steps","predicted_Price","model_vrs",]


class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DemandPrice.objects.order_by("-target_time")
    serializer_class = DemandPriceSerializer

    @action(detail=False, methods=["post"])
    def run_now(self, request):
        saved = run_get_Price()
        data = DemandPriceSerializer(saved, many=True).data
        return Response(
            {
                "detail": "Demand Price run completed.",
                "count": len(saved),
                "results": data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def latest(self, request):
        qs = (
            DemandPrice.objects.filter(horizon_steps=12)
            .order_by("-target_time")[:13]
        )
        if not qs.exists():
            return Response([])

        return Response(DemandPriceSerializer(qs, many=True).data)