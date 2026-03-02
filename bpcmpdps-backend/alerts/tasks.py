from celery import shared_task
from django.utils import timezone

from accounts.models import OperatorProfile
from .models import AlertDelivery
from .sms import send_sms

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