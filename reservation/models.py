from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField

from base_data.models import City, Job
from reservation.fields import PercentageField

class PaymentPolicy(models.Model):
    reservation_percentage = PercentageField()
    refund_percentage = PercentageField()
    business_owner = models.OneToOneField("BusinessOwner", on_delete=models.CASCADE, related_name="payment_policy",
                                          primary_key=True)


class BusinessOwner(models.Model):
    ONLINE = 'O'
    PHONE_CALL = 'PC'
    ONLINE_AND_PHONE_CALL = 'OPC'

    RESERVATION_TYPE = [
        (ONLINE, "online"),
        (PHONE_CALL, "phone_call"),
        (ONLINE_AND_PHONE_CALL, "online and phone call"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_owner")
    self_description = models.TextField(null=True, blank=True)
    reservation_type = models.CharField(choices=RESERVATION_TYPE, default=ONLINE_AND_PHONE_CALL, max_length=3)
    address = models.TextField(null=True, blank=True)
    phone_number = PhoneNumberField(region="IR", null=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="business_owner", null=True, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, related_name="business_owner",
                            null=True, blank=True)
    default_appointment_price = models.PositiveIntegerField(null=True, blank=True)
    default_appointment_duration = models.PositiveSmallIntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True,
                                        blank=True)


class BOFile(models.Model):
    file = models.FileField(upload_to='files')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(BusinessOwner, models.CASCADE, related_name="files")


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer")
    business_owner_list = models.ManyToManyField(BusinessOwner, blank=True)


class Comment(models.Model):
    value = models.TextField(blank=False)
    comment_on = models.ForeignKey(BusinessOwner, models.CASCADE, related_name="comments_for_me")
    commenter = models.ForeignKey(Customer, models.CASCADE, related_name="comments")


@receiver(post_save, sender=BusinessOwner)
def create_payment_policy(sender, instance=None, created=False, **kwargs):
    if created:
        PaymentPolicy.objects.create(business_owner=instance, reservation_percentage=1, refund_percentage=1)
