from django.contrib import admin
from .models import ThresholdConfig, AlertEvent, AlertDelivery

@admin.register(ThresholdConfig)
class ThresholdConfigAdmin(admin.ModelAdmin):
    list_display = ("user", "demand_kw_threshold", "price_threshold", "updated_at")

@admin.register(AlertEvent)
class AlertEventAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "predicted_demand_kw", "predicted_price", "reason", "status")
    list_filter = ("status",)
    ordering = ("-created_at",)

@admin.register(AlertDelivery)
class AlertDeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "alert_event", "user", "phone_number", "status", "sent_at")
    list_filter = ("status",)
    ordering = ("-id",)