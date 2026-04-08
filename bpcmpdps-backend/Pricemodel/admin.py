from django.contrib import admin
from Model import DemandPrice


@admin.register(DemandPrice)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = (
        "target_time",
        "prediction_time",
        "horizon_steps",
        "predicted_Price",
        "model_vrs",
    )
    list_filter = ("model_vrs", "horizon_steps")
    search_fields = ("model_vrs",)
    ordering = ("-target_time",)