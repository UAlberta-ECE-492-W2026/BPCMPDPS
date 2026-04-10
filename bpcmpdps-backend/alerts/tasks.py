from celery import shared_task
from django.utils import timezone

from accounts.models import OperatorProfile
from .models import AlertDelivery, AlertEvent, ThresholdConfig
from .sms import send_sms


@shared_task
def check_thresholds_and_alert():
    """
    Runs after both forecast + price pipelines each hour.
    Grabs the latest demand and price predictions, then checks
    every user's thresholds. Fires SMS alerts when exceeded.
    """
    from forecasting.models import DemandForecast
    from Pricemodel.Model import DemandPrice

    # Get the most recent h12 demand prediction
    latest_demand = (
        DemandForecast.objects.filter(horizon_steps=12)
        .order_by("-target_time")
        .first()
    )
    # Get the most recent h12 price prediction
    latest_price = (
        DemandPrice.objects.filter(horizon_steps=12)
        .order_by("-target_time")
        .first()
    )

    demand_kw = latest_demand.predicted_demand_kw if latest_demand else 0.0
    price = latest_price.predicted_Price if latest_price else 0.0

    # Get all users who have alerts enabled + a phone number
    profiles = OperatorProfile.objects.filter(
        alerts_enabled=True,
    ).exclude(phone_number="")

    if not profiles.exists():
        return {"detail": "No users with alerts enabled."}

    alerts_sent = 0

    for profile in profiles:
        # Get this user's latest threshold config
        cfg = ThresholdConfig.objects.filter(user=profile.user).first()
        if cfg is None:
            continue

        demand_hit = demand_kw >= cfg.demand_kw_threshold
        price_hit = price >= cfg.price_threshold

        if not (demand_hit or price_hit):
            continue

        reasons = []
        if demand_hit:
            reasons.append("demand")
        if price_hit:
            reasons.append("price")
        reason_text = f"Threshold exceeded: {', '.join(reasons)}"

        alert = AlertEvent.objects.create(
            predicted_demand_kw=demand_kw,
            predicted_price=price,
            reason=reason_text,
            status="CREATED",
        )

        delivery = AlertDelivery.objects.create(
            alert_event=alert,
            user=profile.user,
            phone_number=profile.phone_number,
            status="PENDING",
        )

        sms_body = (
            f"[BPCMPDPS] {reason_text}\n"
            f"Demand={demand_kw:.1f} kW (thr {cfg.demand_kw_threshold:.1f}), "
            f"Price=${price:.2f} (thr ${cfg.price_threshold:.2f})"
        )

        send_alert_sms.delay(delivery.id, sms_body)
        alerts_sent += 1

    return {"alerts_sent": alerts_sent}


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_alert_sms(self, delivery_id: int, sms_body: str):
    delivery = AlertDelivery.objects.select_related("alert_event", "user").get(id=delivery_id)
    profile = OperatorProfile.objects.get(user=delivery.user)

    try:
        sid = send_sms(profile.phone_number, sms_body)
        delivery.status = "SENT"
        delivery.provider_message_id = sid
        delivery.sent_at = timezone.now()
        delivery.save(update_fields=["status", "provider_message_id", "sent_at"])

        event = delivery.alert_event
        event.status = "SENT"
        event.save(update_fields=["status"])
        return {"sid": sid}
    except Exception as e:
        delivery.status = "FAILED"
        delivery.error = str(e)
        delivery.save(update_fields=["status", "error"])
        raise self.retry(exc=e)