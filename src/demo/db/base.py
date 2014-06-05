from demo.handler import demo_request

__author__ = 'Maxaon'

from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper
from django.db.backends.sqlite3.base import *
import os
import hashlib
import shutil


def remember_cookie(cookie, **kwargs):
    remember_cookie.cookie = hashlib.md5(cookie).hexdigest()


remember_cookie.cookie = None

demo_request.connect(remember_cookie)


class DatabaseWrapper(SQLiteDatabaseWrapper):
    def get_connection_params(self):
        params = super(DatabaseWrapper, self).get_connection_params()
        if 'DEMO_PATH' in self.settings_dict and remember_cookie.cookie:
            demo_path = self.settings_dict['DEMO_PATH']
            # if not os.path.isdir(demo_path):
            # os.makedirs(demo_path)
            src = params['database']
            # name = os.path.basename(params['database'])
            dst = os.path.join(demo_path, remember_cookie.cookie)
            if not os.path.isfile(dst):
                shutil.copy(src, dst)
            params['database'] = dst
        return params