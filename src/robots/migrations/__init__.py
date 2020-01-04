"""
Django migrations for robots app

This package does not contain South migrations. South migrations can be found
in the ``south_migrations`` package.
"""

# This check is based on code from django-email-log. Thanks Trey Hunner.
# https://github.com/treyhunner/django-email-log/blob/master/email_log/migrations/__init__.py

SOUTH_ERROR_MESSAGE = """\n
For South support, customize the SOUTH_MIGRATION_MODULES setting like so:

    SOUTH_MIGRATION_MODULES = {
        'robots': 'robots.south_migrations',
    }
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    from django.db import migrations  # noqa
except ImportError:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
