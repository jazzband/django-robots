import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    return open(path.join(path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-robots',
    long_description=read('docs', 'index.txt'),
    version=find_version('robots', '__init__.py'),
    description='Robots exclusion application for Django, complementing Sitemaps.',
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='https://github.com/jezdez/django-robots/',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'robots': [
            'locale/*/LC_MESSAGES/*',
            'templates/robots/*.html',
        ],
    },
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
    ]
)
