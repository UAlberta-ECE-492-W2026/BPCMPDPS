from django.db import models


class DemandForecast(models.Model):
    prediction_made_at = models.DateTimeField(db_index=True)
    target_time = models.DateTimeField(db_index=True)
    horizon_steps = models.IntegerField()
    predicted_demand_kw = models.FloatField()
    model_version = models.CharField(max_length=100, default="v1")

    class Meta:
        ordering = ["target_time"]
        unique_together = ("prediction_made_at", "target_time", "horizon_steps")

    def __str__(self):
        return f"{self.target_time} -> {self.predicted_demand_kw:.2f} kW"