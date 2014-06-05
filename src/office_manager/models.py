from django.db import models
from django.contrib.contenttypes.generic import GenericRelation
from secret_storage.models import EncryptedRecords
from django.conf import settings

__author__ = 'Maxaon'


class Citizens(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    data = GenericRelation(EncryptedRecords)


class Payments(models.Model):
    citizen = models.ForeignKey(Citizens)
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    payment_date = models.DateTimeField(auto_now=True)
    payment_type = models.IntegerField(choices=(
        (1, "Cash"),
        (2, 'Card')
    ))
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL)

