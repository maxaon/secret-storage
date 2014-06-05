# !/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), '')
    sys.path.append(path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secret_storage.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
