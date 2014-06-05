import gpg
from rest_framework import status
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework.decorators import action, link
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from secret_storage.routes import collection_action, collection_link
from secret_storage.serializers import PublicKeysSerializer, UsersSerializer
from django.conf import settings

__author__ = 'Maxaon'


def get_key_id(key):
    from openpgp.sap.armory import list_armored
    from openpgp.sap.list import list_pkts
    from openpgp.sap.pkt.PublicKey import PublicKey

    res = list_armored(key)
    if len(res) != 1:
        raise ParseError("Wrong key")
    keys = list_pkts(res[0].data)
    if len(keys) != 5 or not isinstance(keys[0], PublicKey):
        raise ParseError("Unknown key format")
    secret_key = keys[0].body
    return secret_key.id


class PublicKeySerializerView(ModelViewSet):
    model = PublicKeysSerializer.Meta.model
    serializer_class = PublicKeysSerializer

    def pre_save(self, obj):
        super(PublicKeySerializerView, self).pre_save(obj)
        if self.request.DATA['public_key']:
            keyid = get_key_id(self.request.DATA['public_key'])
            assert len(keyid) == 16
            obj.keyid = keyid


class UserViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    model = get_user_model()

    @collection_link()
    def current(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @collection_action(['get', 'post'])
    def authorize(self, request, *args, **kwargs):
        if request.method.lower() == 'get':
            authenticate()
            return Response(data={"ans": "Collection action"})
        else:
            user = authenticate(username=request.DATA['username'], password=request.DATA['password'])
            if not user:
                raise AuthenticationFailed()
            login(request, user)

            serializer = self.get_serializer(user)
            return Response(data=serializer.data)

    def check_permissions(self, request):
        try:
            super(UserViewSet, self).check_permissions(request)
        except NotAuthenticated:
            # TODO should use permissions
            if (request.method.lower() == 'post'
                and request.path == u'/api/users/authorize'
                and not getattr(request.session, 'data_access_allowed', False)):
                setattr(request.session, 'data_access_allowed', True)  # to disable form display
                return
            else:
                raise

    def pre_save(self, obj):
        psw = self.request.DATA.get('password')
        if psw:
            if len(psw) < 8:
                return Response({"password": ["Password length should be more then 8 symbols"]},
                                status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(psw)
        super(UserViewSet, self).pre_save(obj)


settings.API_ROUTER.register('public-keys', PublicKeySerializerView)
settings.API_ROUTER.register('users', UserViewSet)