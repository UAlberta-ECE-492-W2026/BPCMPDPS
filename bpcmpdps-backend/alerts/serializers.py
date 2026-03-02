from rest_framework import serializers
from .models import ThresholdConfig, AlertEvent

class ThresholdConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThresholdConfig
        fields = ["demand_kw_threshold", "price_threshold", "updated_at"]
        read_only_fields = ["updated_at"]

class TestAlertSerializer(serializers.Serializer):
    demand_kw = serializers.FloatField()
    price = serializers.FloatField()
    dry_run = serializers.BooleanField(default=False)

class AlertEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertEvent
        fields = ["id", "created_at", "predicted_demand_kw", "predicted_price", "reason", "status"]