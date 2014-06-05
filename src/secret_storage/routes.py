from collections import namedtuple
from django.core.exceptions import ImproperlyConfigured
from rest_framework.routers import DefaultRouter, flatten, replace_methodname

__author__ = 'Maxaon'
Route = namedtuple('Route', ['url', 'mapping', 'name', 'initkwargs', 'bind_to_collection'])


def collection_link(**kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for GET requests.
    """

    def decorator(func):
        func.bind_to_methods = ['get']
        func.kwargs = kwargs
        func.bind_to_collection = True
        return func

    return decorator


def collection_action(methods=['post'], **kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for POST requests.
    """

    def decorator(func):
        func.bind_to_methods = methods
        func.kwargs = kwargs
        func.bind_to_collection = True
        return func

    return decorator


class MyMegaRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'},
            bind_to_collection=None
        ),
        # Dynamically generated routes.
        # Generated using @collection_action or @collection_link decorators on methods of the viewset.
        Route(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-collection',
            initkwargs={},
            bind_to_collection=True
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'},
            bind_to_collection=None
        ),
        # Dynamically generated routes.
        # Generated using @action or @link decorators on methods of the viewset.
        Route(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-{methodnamehyphen}',
            initkwargs={},
            bind_to_collection=False
        ),
    ]


    def get_routes(self, viewset):
        """
        Augment `self.routes` with any dynamically generated routes.

        Returns a list of the Route namedtuple.
        """

        known_actions = flatten([route.mapping.values() for route in self.routes])

        # Determine any `@action` or `@link` decorated methods on the viewset
        dynamic_routes = []
        for methodname in dir(viewset):
            attr = getattr(viewset, methodname)
            httpmethods = getattr(attr, 'bind_to_methods', None)
            if httpmethods:
                if methodname in known_actions:
                    raise ImproperlyConfigured('Cannot use @action or @link decorator on '
                                               'method "%s" as it is an existing route' % methodname)
                httpmethods = [method.lower() for method in httpmethods]
                dynamic_routes.append((httpmethods, methodname, getattr(attr, 'bind_to_collection', False)))

        ret = []
        for route in self.routes:
            if route.mapping == {'{httpmethod}': '{methodname}'}:
                # Dynamic routes (@link or @action decorator)
                for httpmethods, methodname, bind_to_collection in dynamic_routes:
                    if bind_to_collection and not route.bind_to_collection or not bind_to_collection and route.bind_to_collection:
                        continue

                    initkwargs = route.initkwargs.copy()
                    initkwargs.update(getattr(viewset, methodname).kwargs)
                    ret.append(Route(
                        url=replace_methodname(route.url, methodname),
                        mapping=dict((httpmethod, methodname) for httpmethod in httpmethods),
                        name=replace_methodname(route.name, methodname),
                        initkwargs=initkwargs,
                        bind_to_collection=bind_to_collection
                    ))
            else:
                # Standard route
                ret.append(route)

        return ret

