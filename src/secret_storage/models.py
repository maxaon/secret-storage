from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class PublicKeys(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, primary_key=True)
    public_key = models.TextField(unique=True)
    keyid = models.CharField(max_length=16, unique=True)
    # fingerprint = models.CharField(max_length=12)


class EncryptedRecords(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    key = models.ForeignKey(PublicKeys)

    encrypted_data = models.TextField()
    signature = models.TextField()

    last_edit = models.DateTimeField(auto_now=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')




