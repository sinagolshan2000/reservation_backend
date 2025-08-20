from django.db import models

from reservation.models import BusinessOwner, Customer


class Appointment(models.Model):
    business_owner = models.ForeignKey(BusinessOwner, models.CASCADE, related_name="appointments")
    customer = models.ForeignKey(Customer, models.CASCADE, related_name="customer_appointments", null=True)
    price = models.PositiveIntegerField()
    payable_price = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
