# coding=utf-8
from collections import OrderedDict
import os
from functools import partial
from json import loads
import unittest

__author__ = 'Maxaon'

import re

join = lambda *path: os.path.abspath(os.path.join(*path))


class BowerPkg(object):
    def __init__(self, name=None, main=None, dependencies=None, pkg=None, **kwargs):
        self.__dependencies = self.__main = None
        if isinstance(name, dict):
            kwargs = name
            name = None

        assert isinstance(name, basestring) or name is None
        self.name = name
        self.main = main
        self.dependencies = dependencies
        self.pkg = pkg
        if kwargs:
            for k, v in kwargs.iteritems():
                setattr(self, k, v)

    @property
    def main(self):
        return self.__main

    @main.setter
    def main(self, value):
        if isinstance(value, basestring):
            value = [value]
        self.__main = value

    @property
    def dependencies(self):
        return self.__dependencies

    @dependencies.setter
    def dependencies(self, value):
        if isinstance(value, basestring):
            value = {value: None}
        elif isinstance(value, (tuple, list)):
            value = dict([(k, None) for k in value])
        assert isinstance(value, dict) or value is None
        self.__dependencies = value

    @property
    def has_missing(self):
        return not (self.name and self.main and self.dependencies)

    def main_rel(self):
        return map(lambda mf: re.sub('/*\./|/+', '/', self.pkg + "/" + mf), self.main)


class BowerFinder(object):
    def __init__(self, root, apps):
        self.root = root
        self.apps = apps
        self.__normalized_config = None

    def _get_custom_normalized_config(self, pkg):
        desc = None
        if pkg in self.apps:
            desc = self.apps[pkg]
        else:
            for pkg_name, pkg_desc in self.apps.iteritems():
                if (isinstance(pkg_desc, dict) and pkg_desc.get('name') == pkg) or (pkg in pkg_name):
                    desc = pkg_desc
                    if isinstance(desc, (list, tuple)):
                        desc = {'main': desc}
                    break
        if not isinstance(desc, dict):
            res = BowerPkg(main=desc)
        else:
            res = BowerPkg(desc)
        res.pkg = pkg
        return res

    @staticmethod
    def load_config(pkg_dir):
        bower_file_path = None
        for applicant in map(partial(join, pkg_dir), ('bower.json', 'component.json', '.bower.json')):
            if os.path.isfile(applicant):
                bower_file_path = applicant
                break
        if bower_file_path is None:
            raise Exception("Main file not found for package '{}'".format(os.path.dirname(pkg_dir)))
        with open(bower_file_path) as f:
            bower_config = f.read()
            bower_config = loads(bower_config)
        return bower_config

    @staticmethod
    def to_list(prop):
        if isinstance(prop, basestring):
            return [prop]
        else:
            return prop

    def _normalize_config(self):
        all_main_files = OrderedDict()
        for pkg in os.listdir(self.root):
            pkg_dir = join(self.root, pkg)
            if not os.path.isdir(pkg_dir):
                continue

            custom_config = self._get_custom_normalized_config(pkg)

            if custom_config.has_missing:
                bower_config = self.load_config(pkg_dir)
                if custom_config.main is None:
                    if 'main' not in bower_config:
                        raise Exception("Configuration for package '{}' doesn't have main property".format(pkg))
                    custom_config.main = bower_config['main']
                if custom_config.dependencies is None:
                    custom_config.dependencies = bower_config.get('dependencies', {})
                if custom_config.name is None:
                    try:
                        custom_config.name = bower_config['name']
                    except KeyError:
                        raise Exception("Package '{}' doen'nt have name".format(pkg))
            all_main_files[custom_config.name] = custom_config
        return self.resolve_dependencies(all_main_files)

    @property
    def normalized_config(self):
        if not self.__normalized_config:
            self.__normalized_config = self._normalize_config()
        return self.__normalized_config

    @staticmethod
    def resolve_dependencies(cfg):
        to_sort = {}
        for pkg in cfg.itervalues():
            to_sort[pkg.name] = (pkg.dependencies or {}).keys()
        t_soted = topologic_sort_dfs2(to_sort)
        result = OrderedDict()
        for key in t_soted:
            result[key] = cfg[key]
        return result

    def get(self, ext):
        if '.' not in ext:
            ext = '.' + ext

        result = []
        for pkg in self.normalized_config.itervalues():
            result.extend(pkg.main_rel())

        return filter(lambda f: f.endswith(ext), result)


def replace_conf(obj, key, search, replace):
    for_replace = list(obj[key]['source_filenames'])
    for i, k in enumerate(for_replace):
        if search in k:
            for_replace[i] = k.replace(search, replace)
            break

            # try:
            # for_replace[for_replace.index(search)] = replace
            # except ValueError:
            # return
    obj[key]['source_filenames'] = for_replace


# Color — массив, в котором хранятся цвета вершин (0 — белый, 1 — серый, 2 — черный).
# Edges — массив списков смежных вершин.
# Numbers — массив, в котором сохраняются новые номера вершин.
# Stack — стек, в котором складываются вершины после их обработки.
# Cycle — принимает значение true, если в графе найден цикл.
# Edges = {'a': ['c'], 'c': ['b'], 'd': ['c', 'b', 't'], 'b': [], 't': []}


def topologic_sort_dfs2(edges):
    stack = []
    color = dict()
    for i in edges.keys():
        color[i] = 0

    def topological_sort():
        def dfs(edge):
            # Если вершина серая, то мы обнаружили цикл.
            # Заканчиваем поиск в глубину.
            if color[edge] == 1: return True
            if color[edge] == 2: return False  # Если вершина черная, то заканчиваем ее обработку.
            color[edge] = 1  # Красим вершину в серый цвет.
            # Обрабатываем список смежных с ней вершин.
            for dep in edges[edge]:
                if dfs(dep): return True
            stack.append(edge)  # Кладем вершину в стек.
            color[edge] = 2  # Красим вершину в черный цвет.
            return False

        # Вызывается обход в глубину от всех вершин.
        # Заканчиваем работу алгоритма, если обнаружен цикл.
        for edge in edges.keys():
            cycle = dfs(edge)
            if cycle:
                raise Exception("Dependency cycle found")

                # Заносим в массив новые номера вершин.
        return stack

    return topological_sort()


class BowerPkgTest(unittest.TestCase):
    def test_kwargs(self):
        obj = BowerPkg({'name': 'Name', 'main': "main.js"})
        self.assertEqual(obj.name, 'Name')
        self.assertEqual(obj.main, ['main.js'])
        obj = BowerPkg(None)
        self.assertIsNone(obj.name)

