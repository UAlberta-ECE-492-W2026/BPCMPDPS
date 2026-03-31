from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import APIView, action
from rest_framework.response import Response

from accounts.models import OperatorProfile
from .models import ThresholdConfig, AlertEvent, AlertDelivery, ActualDemand
from .serializers import ThresholdConfigSerializer, TestAlertSerializer, AlertEventSerializer
from .tasks import send_alert_sms


class ThresholdViewSet(viewsets.ViewSet):
    """
    /api/alerts/thresholds/ (GET, POST)
    """

    def list(self, request):
        cfg, _ = ThresholdConfig.objects.get_or_create(user=request.user)
        return Response(ThresholdConfigSerializer(cfg).data)

    def create(self, request):
        cfg, _ = ThresholdConfig.objects.get_or_create(user=request.user)
        s = ThresholdConfigSerializer(cfg, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)


class AlertViewSet(viewsets.ViewSet):
    """
    /api/alerts/alerts/test/   (POST)
    /api/alerts/alerts/events/ (GET)
    """

    @action(detail=False, methods=["post"])
    def test(self, request):
        s = TestAlertSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        demand_kw = s.validated_data["demand_kw"]
        price = s.validated_data["price"]
        dry_run = s.validated_data["dry_run"]

        cfg, _ = ThresholdConfig.objects.get_or_create(user=request.user)
        demand_hit = demand_kw >= cfg.demand_kw_threshold
        price_hit = price >= cfg.price_threshold

        if not (demand_hit or price_hit):
            return Response({
                "alert_triggered": False,
                "reason": "No thresholds exceeded",
                "thresholds": ThresholdConfigSerializer(cfg).data,
            })

        reasons = []
        if demand_hit: reasons.append("demand")
        if price_hit: reasons.append("price")
        reason_text = f"Threshold exceeded: {', '.join(reasons)}"

        alert = AlertEvent.objects.create(
            predicted_demand_kw=demand_kw,
            predicted_price=price,
            reason=reason_text,
            status="CREATED",
        )

        profile = OperatorProfile.objects.get(user=request.user)
        if not profile.alerts_enabled or not profile.phone_number:
            alert.status = "FAILED"
            alert.save(update_fields=["status"])
            return Response({
                "alert_triggered": True,
                "alert_event": AlertEventSerializer(alert).data,
                "detail": "Alerts disabled or phone number missing (set it in admin)."
            }, status=status.HTTP_400_BAD_REQUEST)

        delivery = AlertDelivery.objects.create(
            alert_event=alert,
            user=request.user,
            phone_number=profile.phone_number,
            status="PENDING",
        )

        sms_body = (
            f"[BPCMPDPS] {reason_text}\n"
            f"Demand={demand_kw:.1f} kW (thr {cfg.demand_kw_threshold:.1f}), "
            f"Price={price:.1f} (thr {cfg.price_threshold:.1f})"
        )

        if dry_run:
            delivery.status = "SENT"
            delivery.sent_at = timezone.now()
            delivery.provider_message_id = "DRY_RUN"
            delivery.save(update_fields=["status", "sent_at", "provider_message_id"])
            alert.status = "SENT"
            alert.save(update_fields=["status"])
            return Response({
                "alert_triggered": True,
                "dry_run": True,
                "alert_event": AlertEventSerializer(alert).data,
                "delivery_status": delivery.status,
            })

        send_alert_sms.delay(delivery.id, sms_body)

        return Response({
            "alert_triggered": True,
            "queued": True,
            "alert_event": AlertEventSerializer(alert).data,
            "delivery_id": delivery.id,
        })

    @action(detail=False, methods=["get"])
    def events(self, request):
        qs = AlertEvent.objects.order_by("-created_at")[:50]
        return Response(AlertEventSerializer(qs, many=True).data)