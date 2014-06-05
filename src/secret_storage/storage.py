import os
from django.conf import settings

__author__ = 'Maxaon'
from pipeline.storage import PipelineCachedStorage, PipelineMixin, CachedStaticFilesStorage, StaticFilesStorage


class TempStorage(StaticFilesStorage):
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        location = location or settings.TEMP_ROOT
        super(TempStorage, self).__init__(location, base_url, *args, **kwargs)


class PublicCachedStorage(CachedStaticFilesStorage):
    packing = True

    def __init__(self, *args, **kwargs):
        super(PublicCachedStorage, self).__init__(*args, **kwargs)
        self.to_process_paths = None
        self.additionaly_processed = None

    def post_process(self, paths, dry_run=False, **options):
        # return super(PublicCachedStorage, self).post_process(paths, dry_run, **options)
        if dry_run:
            return

        from pipeline.packager import Packager

        storage = options.get('temp_storage', self)
        storage = self
        self.to_process_paths = paths
        self.additionaly_processed = []

        packager = Packager(storage=storage)
        packed_path = {}
        packed = []
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_stylesheets(package)
            packed_path[output_file] = (storage, output_file)
            packed.append((output_file, output_file, True))
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_javascripts(package)
            packed_path[output_file] = (storage, output_file)
            packed.append((output_file, output_file, True))

        cached = []
        ex = []
        super_class = super(PublicCachedStorage, self)
        if hasattr(super_class, 'post_process'):
            for ppp in packed_path:
                try:
                    for name, hashed_name, processed in super_class.post_process({ppp: packed_path[ppp]},
                                                                                 dry_run, **options):
                        if isinstance(processed, Exception):
                            ex.append(processed)
                        cached.append((name, hashed_name, processed))
                except Exception as e:
                    ex.append(e)
                    continue

                    # for name, hashed_name, processed in super_class.post_process(packed_path.copy(), dry_run, **options):

                    # cached.append((name, hashed_name, processed))

        if ex:
            raise ex[0]

        for f in cached:
            yield f

    def hashed_name(self, name, content=None):
        try:
            return super(PublicCachedStorage, self).hashed_name(name, content)
        except ValueError as ex:
            if self.to_process_paths:
                try:
                    if "?" in name:
                        name = name[:name.index("?")]
                    name = name.replace("/", os.sep)
                    for name, hashed_name, processed in super(PublicCachedStorage, self).post_process(
                            {name: self.to_process_paths[name]}):
                        if isinstance(processed, Exception):
                            raise processed
                        self.additionaly_processed.append((name, hashed_name, processed))
                        return hashed_name
                except Exception as ex2:
                    raise ex
                    # return self.hashed_name(name, content)
            else:
                raise ex

    def url(self, name, force=False):
        try:
            return super(PublicCachedStorage, self).url(name, force)
        except ValueError:
            return ""



