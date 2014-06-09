from __future__ import with_statement
import pprint
import subprocess
from collections import OrderedDict
from re import search
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils.encoding import smart_bytes
from djangobower.bower import BowerAdapter
import os
from djangobower.conf import BOWER_PATH, COMPONENTS_ROOT
from os.path import join
import re
from itertools import izip_longest
from secret_storage.shortcuts.bower_finder import extract_bower_name

__author__ = 'Maxaon'


def execute_command(command, content=None, cwd=None):
    import subprocess

    pipe = subprocess.Popen(command, cwd=cwd,
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if content:
        content = smart_bytes(content)
    stdout, stderr = pipe.communicate(content)
    if stderr.strip():
        raise Exception(stderr)
    return stdout


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        requirements = None
        try:
            requirements = settings.REQUIREMENTS_FILE
        except AttributeError:
            pass
        if not requirements and os.path.isfile("requirements.txt"):
            requirements = os.path.abspath("requirements.txt")

        self.freeze_pip(requirements)
        self.freeze_bower()


    def freeze_pip(self, requirements):
        packages = execute_command(['pip', 'freeze'])
        with open(requirements, "w") as f:
            f.write(packages)

    def freeze_bower(self):


        adapter = BowerAdapter(BOWER_PATH, COMPONENTS_ROOT)
        packages = list(adapter.freeze())
        packages_norm = dict(zip(map(extract_bower_name, packages), packages))
        user_pkgs = settings.BOWER_INSTALLED_APPS
        res = {}
        for n, d in map(lambda d: (extract_bower_name(d[0]), d), user_pkgs.iteritems()):
            if n in packages_norm:
                res[packages_norm[n]] = d[1]
                del packages_norm[n]
            else:
                res[n] = d[1]
        res.update(izip_longest(packages_norm.values(), []))
        a = pprint.pformat(res, 4).replace("{", "{\n").replace("}", "\n}")
        a = 'BOWER_INSTALLED_APPS = ' + a

        ind = [0]

        def p(line):
            ind[0] -= line.count("}")
            line = ind[0] * 4 * " " + line.strip()
            ind[0] += line.count('{')
            return line + "\n"

        # g = map(p, a.split("\n"))

        a = map(p, a.split("\n"))
        settings_path = os.path.join(settings.PROJECT_PATH, "settings.py")
        new_set = []
        with open(settings_path) as s:
            incfg = False
            brc = 0
            r = re.compile('BOWER_INSTALLED_APPS\s=')
            for line in s.readlines():
                if r.match(line):
                    incfg = True
                    new_set.extend(a)
                if incfg:
                    brc = brc + line.count('{') - line.count("}")
                if incfg and brc == 0:
                    incfg = False
                    continue

                if not incfg:
                    new_set.append(line)
        try:
            os.unlink(settings_path + ".bak")
        except OSError:
            pass

        os.rename(settings_path, settings_path + ".bak")

        with open(settings_path, "w") as s:
            s.writelines(new_set)

        return a













