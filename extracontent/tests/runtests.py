#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings

from django.test.simple import run_tests

if __name__ == "__main__":
    failures = run_tests(['extracontent'], verbosity=1)
    if failures:
        sys.exit(failures)