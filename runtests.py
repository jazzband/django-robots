#!/usr/bin/env python

import sys


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'robots',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        }
    },
    ROOT_URLCONF='tests.test_utils.urls',
    SITE_ID=1,
    MIDDLEWARE_CLASSES=[
        'django.middleware.http.ConditionalGetMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
)


def runtests():
    import django
    from django.conf import settings

    # Compatibility with Django 1.7's stricter initialization
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    if hasattr(django, 'setup'):
        django.setup()

    from django.test.runner import DiscoverRunner
    test_args = ['tests']
    failures = DiscoverRunner(
            verbosity=1, interactive=True, failfast=False
    ).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
