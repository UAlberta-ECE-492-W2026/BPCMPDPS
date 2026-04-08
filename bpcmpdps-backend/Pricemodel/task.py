from celery import shared_task
from .service import run_get_Price


@shared_task
def run_price_pipeline():
    saved =run_get_Price()
    return {
        "num_saved": len(saved),
    }