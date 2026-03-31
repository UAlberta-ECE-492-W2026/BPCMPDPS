from celery import shared_task
from .services import run_demand_forecast


@shared_task
def run_forecasting_pipeline():
    saved = run_demand_forecast()
    return {
        "num_saved": len(saved),
    }