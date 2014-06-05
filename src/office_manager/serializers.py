from office_manager.models import Citizens, Payments
from rest_framework.serializers import ModelSerializer
from secret_storage.serializers import EncryptedStorageField

__author__ = 'Maxaon'


class CitizensSerializer(ModelSerializer):
    data = EncryptedStorageField()

    class Meta:
        model = Citizens


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments