from __future__ import unicode_literals
from json.encoder import JSONEncoder
from django.conf import settings
from django.core.management.base import NoArgsCommand
from json import dump, dumps


__author__ = 'Maxaon'
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticComand


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        return "Not serializable"


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        res = dict()
        for prop in dir(settings):
            if prop.startswith("__"):
                continue
            val = getattr(settings, prop)
            res[prop] = val

        dump(res, self.stdout, cls=CustomJSONEncoder)



