from django.contrib import admin
from .models import DemandForecast


@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = (
        "target_time",
        "prediction_made_at",
        "horizon_steps",
        "predicted_demand_kw",
        "model_version",
    )
    list_filter = ("model_version", "horizon_steps")
    search_fields = ("model_version",)
    ordering = ("-target_time",)