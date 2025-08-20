from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CUSTOMER = 'CTR'
    BUSINESS_OWNER = 'BO'
    NA = 'N/A'

    ROLES = [
        (NA, "N/A"),
        (CUSTOMER, "Customer"),
        (BUSINESS_OWNER, "Business Owner"),
    ]

    role = models.CharField(choices=ROLES, max_length=3, default=NA)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
