from __future__ import unicode_literals
from operator import methodcaller, itemgetter
import re
import os
import sys
from optparse import make_option
from django.conf import settings
import fnmatch
from django.core.files.storage import FileSystemStorage
from django.core.management.base import CommandError, NoArgsCommand
from django.utils.encoding import smart_text
from django.utils.datastructures import SortedDict

from django.contrib.staticfiles import finders, storage
from secret_storage.storage import TempStorage

__author__ = 'Maxaon'
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticComand


class Command(CollectStaticComand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.copied_files = []
        self.symlinked_files = []
        self.unmodified_files = []
        self.post_processed_files = []
        self.base_storage = storage.staticfiles_storage
        self.storage = TempStorage()

        settings.STATICFILES_DIRS = settings.STATICFILES_DIRS + (self.storage.location,)

        try:
            self.storage.path('')
        except NotImplementedError:
            self.local = False
        else:
            self.local = True

    def collect(self):
        """
        Perform the bulk of the work of collectstatic.

        Split off from handle_noargs() to facilitate testing.
        """
        if self.symlink:
            if sys.platform == 'win32':
                raise CommandError("Symlinking is not supported by this "
                                   "platform (%s)." % sys.platform)
            if not self.local:
                raise CommandError("Can't symlink to a remote destination.")

        if self.clear:
            self.clear_dir('', self.base_storage)
            self.clear_dir('')

        if self.symlink:
            handler = self.link_file
        else:
            handler = self.copy_file

        to_copy = self.get_allowed_files()
        not_sutible = SortedDict()
        found_files = SortedDict()
        for finder in finders.get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                # Prefix the relative path if the source storage contains it
                if getattr(storage, 'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path

                path_neormalized = path.replace("\\", '/')
                # if not any((r.match(path_neormalized) for r in to_copy)):
                # not_sutible[prefixed_path] = (storage, path)
                if prefixed_path not in found_files:
                    # for ext in ('.css', '.js'):
                    # if path.endswith(ext) and not path.endswith('.min' + ext):
                    # possible_path = path[:-len(ext)] + ".min" + ext
                    # if storage.exists(possible_path):
                    # path = possible_path
                    found_files[prefixed_path] = (storage, path)
                    handler(path, prefixed_path, storage)

        # Here we check if the storage backend has a post_process
        # method and pass it the list of modified files.
        if self.post_process and hasattr(self.base_storage, 'post_process'):
            processor = self.base_storage.post_process(found_files,
                                                       dry_run=self.dry_run, temp_storage=self.storage)
            for original_path, processed_path, processed in processor:
                if isinstance(processed, Exception):
                    self.stderr.write("Post-processing '%s' failed!" % original_path)
                    # Add a blank line before the traceback, otherwise it's
                    # too easy to miss the relevant part of the error message.
                    self.stderr.write("")
                    raise processed
                if processed:
                    self.log("Post-processed '%s' as '%s'" %
                             (original_path, processed_path), level=1)
                    self.post_processed_files.append(original_path)
                else:
                    self.log("Skipped post-processing '%s'" % original_path)

        return {
            'modified': self.copied_files + self.symlinked_files,
            'unmodified': self.unmodified_files,
            'post_processed': self.post_processed_files,
        }

    @staticmethod
    def get_allowed_files():
        res = []
        for cfg in (settings.PIPELINE_CSS, settings.PIPELINE_JS):
            for src in map(itemgetter('source_filenames'), cfg.values()):
                res.extend(src)

        def to_re(s):
            s = s.replace("**/", "*")
            r = fnmatch.translate(s)
            return re.compile(r)

        return map(to_re, res)


    def clear_dir(self, path, st=None):
        """
        Deletes the given relative path using the destination storage backend.
        """
        st = st or self.storage
        dirs, files = st.listdir(path)
        for f in files:
            fpath = os.path.join(path, f)
            if self.dry_run:
                self.log("Pretending to delete '%s'" %
                         smart_text(fpath), level=1)
            else:
                self.log("Deleting '%s'" % smart_text(fpath), level=1)
                st.delete(fpath)
        for d in dirs:
            self.clear_dir(os.path.join(path, d), st)


