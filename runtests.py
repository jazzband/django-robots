import os
import sys
import unittest
from os.path import dirname, abspath
from optparse import OptionParser

sys.path.insert(0, dirname(abspath(__file__)))

from django.conf import settings
if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_test'

from django_nose import NoseTestSuiteRunner


class TestsWrapper(unittest.TestCase):
    def __init__(self, *test_args, **kwargs):
        super(TestsWrapper, self).__init__()
        from django.conf import settings
        if not settings.configured:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_test'
        if 'south' in settings.INSTALLED_APPS:
            from south.management.commands import patch_for_test_db_setup
            patch_for_test_db_setup()
        if not test_args:
            test_args = ['robots.tests']
            kwargs.setdefault('interactive', False)
            test_runner = NoseTestSuiteRunner(**kwargs)
            self._failures = test_runner.run_tests(test_args)

    def runTest(self):
        self.assertEqual(self._failures, 0)

def runtests(*args, **kwargs):
    return TestsWrapper(*args, **kwargs)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--verbosity', dest='verbosity', action='store',
                      default=1, type=int)
    parser.add_options(NoseTestSuiteRunner.options)
    (options, args) = parser.parse_args()
    TestsWrapper(*args, **options.__dict__)