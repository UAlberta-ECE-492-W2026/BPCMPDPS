from django.conf import settings
from django.db import models

class ThresholdConfig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threshold_configs")
    demand_kw_threshold = models.FloatField(default=500.0)
    price_threshold = models.FloatField(default=150.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"ThresholdConfig(user={self.user_id}, created={self.created_at})"

class AlertEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    window_start = models.DateTimeField(null=True, blank=True)
    window_end = models.DateTimeField(null=True, blank=True)

    predicted_demand_kw = models.FloatField()
    predicted_price = models.FloatField()

    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=16,
        choices=[("CREATED", "CREATED"), ("SENT", "SENT"), ("FAILED", "FAILED")],
        default="CREATED",
    )

    def __str__(self):
        return f"AlertEvent(id={self.id}, status={self.status})"

class AlertDelivery(models.Model):
    alert_event = models.ForeignKey(AlertEvent, on_delete=models.CASCADE, related_name="deliveries")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=32)
    provider = models.CharField(max_length=32, default="twilio")
    provider_message_id = models.CharField(max_length=128, blank=True)

    status = models.CharField(
        max_length=16,
        choices=[("PENDING", "PENDING"), ("SENT", "SENT"), ("FAILED", "FAILED")],
        default="PENDING",
    )
    error = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"AlertDelivery(id={self.id}, status={self.status})"
    

class ActualDemand(models.Model):
    timestamp = models.DateTimeField()
    actual_kw = models.FloatField(null=True, blank=True)
    modeled_kw = models.FloatField(null=True, blank=True)
    market_price = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['timestamp']


class EnergyReading(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    uptime_ms = models.BigIntegerField()
    wh = models.IntegerField()
    total_wh = models.IntegerField()

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"EnergyReading(id={self.id}, total_wh={self.total_wh}, received={self.received_at})"

