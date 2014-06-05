from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from secret_storage.models import PublicKeys, EncryptedRecords
from django.conf import settings

__author__ = 'Maxaon'
from rest_framework import serializers


class EncryptedStorageField(serializers.RelatedField):
    empty = None
    read_only = False

    def validate(self, value):


        return super(EncryptedStorageField, self).validate(value)

    def field_to_native(self, obj, field_name):

        """
        Given and object and a field name, returns the value that should be
        serialized for that field.
        """
        if obj is None:
            return self.empty

        if self.source == '*':
            return self.to_native(obj)

        source = self.source or field_name

        curretn_user = self.context['request'].user
        manager = getattr(obj, source)
        try:
            value = manager.get(user=curretn_user)
            value = value.encrypted_data
        except EncryptedRecords.DoesNotExist:
            value = self.empty

        return self.to_native(value)

    def from_native(self, value):
        assert isinstance(value, dict)

        records = []
        request = self.context['request']
        keys = {}
        for key in PublicKeys.objects.all():
            keys[key.keyid] = key
        used_keys = []
        for key, msg in value.iteritems():
            key = key.upper()
            record = EncryptedRecords()

            if not key in keys:
                raise ValidationError("Key with id '{}' not found".format(key))
            if key in used_keys:
                raise ValidationError("Tried to add record with same key id '{}'".format(key))
            used_keys.append(key)

            record.key = keys[key]
            record.user = record.key.user

            record.encrypted_data = msg
            record.signature = ""
            record.editor = request.user
            records.append(record)
        return records

    def field_from_native(self, data, files, field_name, into):
        super(EncryptedStorageField, self).field_from_native(data, files, field_name, into)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'is_superuser',
                  'last_login')


class PublicKeysSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = PublicKeys
        fields = ('user', 'public_key', 'keyid')
        read_only_fields = ('keyid',)
