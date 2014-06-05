class ApiRouter(object):
    def __init__(self, cls, *args, **kwargs):
        self._cls = cls
        self._args = args
        self._kwargs = kwargs
        self._properties = []
        self._registry = []
        self._obj = None

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super(ApiRouter, self).__setattr__(name, value)
        else:
            self._properties.append((name, value))

    def register(self, prefix, viewset, base_name=None):
        self._registry.append((prefix, viewset, base_name))

    def create(self):
        if not self._obj:
            from django.utils.importlib import import_module

            dot = self._cls.rindex('.')
            module = self._cls[:dot]
            class_name = self._cls[dot + 1:]
            cls = getattr(import_module(module), class_name)

            obj = cls(*self._args, **self._kwargs)
            for k, v in self._properties:
                setattr(obj, k, v)
            for prefix, viewset, base_name in self._registry:
                obj.register(prefix, viewset, base_name)
            self._obj = obj
        return self._obj

    @property
    def urls(self):
        return self.create().urls


def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    reouter = settings.API_ROUTER

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        before_import_registry = copy.copy(reouter._registry)
        try:
            import_module('%s.views_rest' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            reouter._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'views_rest'):
                raise
