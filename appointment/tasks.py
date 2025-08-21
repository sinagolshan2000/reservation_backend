from celery import shared_task
from django.utils import timezone
from datetime import datetime
from .models import Appointment

@shared_task
def deactivate_expired_appointments():
    return Appointment.objects.filter(
        date_time__lt=datetime.now(tz=timezone.utc)
    ).update(is_active=False)
