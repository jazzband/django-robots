INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'robots',
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CMS_PERMISSION = True
STATIC_ROOT = '/static/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'urls_test'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

)

import os
HERE = os.path.dirname(os.path.realpath(__file__))
gettext = lambda s: s

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(HERE, 'test-templates'),
)
from djangotoolbox.utils import make_tls_property
from django.conf import settings
settings.__class__.SITE_ID = make_tls_property()
settings.__class__.SITE_ID.value = 1

CMS_TEMPLATES = (
    ('test.html', gettext('test one')),
)
