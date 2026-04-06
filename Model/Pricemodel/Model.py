from django.db import models


class DemandPrice(models.Model):
    prediction_time = models.DateTimeField(db_index=True)
    target_time = models.DateTimeField(db_index=True)
    horizon_steps = models.IntegerField()
    predicted_Price= models.FloatField()
    model_vrs = models.CharField(max_length=100, default="v1")

    class Meta:
        ordering = ["target_time"]
        unique_together = ("prediction_time", "target_time", "horizon_steps")

    def __str__(self):
        return f"{self.target_time} -> {self.predicted_Price:.2f} $"