from __future__ import unicode_literals
from django.conf import settings
from pipeline.storage import TempStorage
from secret_storage.storage import PublicCachedStorage

import os
import sys
from optparse import make_option

from django.core.files.storage import FileSystemStorage
from django.core.management.base import CommandError, NoArgsCommand
from django.utils.encoding import smart_text
from django.utils.datastructures import SortedDict
from django.utils.functional import LazyObject

from django.contrib.staticfiles import finders, storage


__author__ = 'Maxaon'
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticComand


class Command(CollectStaticComand):
    def __init__(self, *args, **kwargs):
        settings.STATICFILES_STORAGE = 'pipeline.storage.TempStorage'
        super(Command, self).__init__(*args, **kwargs)
        self.storage = TempStorage(subfolder="collect")

    # def handle_noargs(self, **options):
    # super(Command, self).handle_noargs(**options)
    #
    #
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
            self.clear_dir('')

        if self.symlink:
            handler = self.link_file
        else:
            handler = self.copy_file

        found_files = SortedDict()
        for finder in finders.get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                # Prefix the relative path if the source storage contains it
                if getattr(storage, 'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path

                if prefixed_path not in found_files:
                    found_files[prefixed_path] = (storage, path)
                    handler(path, prefixed_path, storage)

        # Here we check if the storage backend has a post_process
        # method and pass it the list of modified files.
        pst = PublicCachedStorage(location=settings.STATIC_ROOT)
        processor = pst.post_process(found_files,
                                     dry_run=self.dry_run)
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






