from office_manager.serializers import CitizensSerializer, PaymentsSerializer
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

__author__ = 'Maxaon'


class CitizensViewSet(ModelViewSet):
    serializer_class = CitizensSerializer
    model = serializer_class.Meta.model


class PaymentsViewSet(ModelViewSet):
    serializer_class = PaymentsSerializer
    model = serializer_class.Meta.model


settings.API_ROUTER.register('citizens', CitizensViewSet)
settings.API_ROUTER.register('payments', PaymentsViewSet)