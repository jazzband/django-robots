CHANGES
=======

master (unreleased)
-------------------
*This is where upcoming changes will be.*

6.0 (unreleased)
----------------

Breaking change: Missing ``DEFAULT_AUTO_FIELD``
"""""""""""""""""""""""""""""""""""""""""""""""
This sets a ``DEFAULT_AUTO_FIELD`` to ``BigAutoField`` for robots in ``AppConfig``. Previously,
there was no app configuration or setting for this. (#134, thank you @jan-szejko-steelseries)

Robots 5.0 included a ``BigAutoField`` migration file for django 3.2 support (see #112),
however, this caused an extra migration to be created to set ``django.db.models.AutoField``
for certain users (see #124).

**Breaking: Migration issues**

New django sites should work fine.

*Existing sites that manually created migrations for robots 5.0:*

If you ran ``./manage.py makemigrations`` to bypass the #112 issue, you may need to resolve
this manually if a custom migration you made for robots was applied in ``django_migrations``.

Resources:
- https://docs.djangoproject.com/en/4.1/releases/3.2/#customizing-type-of-auto-created-primary-keys
- https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-DEFAULT_AUTO_FIELD

Maintenance
"""""""""""
- Remove django-south migrations folder (#138)

5.0 (2022-01-08)
----------------
- Dropped support for Python 2.7, 3.5, and 3.6
- Added support for Python 3.9
- Added support for Python 3.10 (#113), thank you @Andrew-Chen-Wang
- Dropped support for Django versions 2.1 and below
- Dropped support for Django 3.0
- Added suppport for Django 3.1
- Added suppport for Django 3.2
- Added support for Django 4.0 (#112), thank you @umarmughal824
- Improve documentation for Django 4.0 (#119), thank you @sergioisidoro
- Sync files with @jazzband/.github
- Add *.pre-commit-config.yaml* and run autofixes (#122)

4.0 (2020-01-04)
-----------------

- Support for Django 2.1, 2.2, 3.0 and Python 3.7 and 3.8.
- Updated the requirements for dropped support of six in Django 3.
- Restructure test setup to use setuptools-scm and more modern Python
  patterns.

3.1.0 (2017-12-11)
------------------

- Add this changelog file
- Support for Django 2.0 via GH-83, fixes GH-81, GH-79
- Drop support for Django 1.10 and below. For older Django versions,
  use django-robots 3.0.0 and below
- Fix docs to include README in index instead of duplicating

3.0 (2017-02-28)
----------------

- Dropped support for Django < 1.8
- Added support for Django 1.10 / 1.11
- Improved admin changeform
- Added support for protocol prefix to Host directive
- Added support for sitemap named views (for non standard sitemap views)
- Fixed an error which resulted in doubling the scheme for sitemap
- Fixed support for cached sitemaps

2.0 (2016-02-28)
----------------

- Dropped support for Django 1.5
- Added support for Django 1.9
- Improved code / metadata quality
- Added Host directive
- Added support to detect current site via http host var
- Added filter_horizontal for for allowed and disallowed
- Fixed error in which get_sitemap_urls modifies SITEMAP_URLS
- Url patterns marked as safe in template
- disabled localization of decimal fields in template

1.1 (2015-05-12)
----------------

- Fixed compatibility to Django 1.7 and 1.8.

- Moved South migrations into different subdirectory so South>=1.0 is needed.

1.0 (2014-01-16)
----------------

- *BACKWARDS-INCOMPATIBLE* change: The default behaviour of this app has
  changed to **allow all bots** from the previous opposite behavior.

- Fixed some backward compatibility issues.

- Updated existing translations (Danish, German, French,
  Portugese (Brasil), Russian).

- Added Greek, Spanish (Spain), Japanese, Dutch, Slovak and Ukrainian
  translations.

0.9.2 (2013-03-24)
------------------

- Fixed compatibility with Django 1.5. Thanks, Russell Keith-Magee.

0.9.1 (2012-11-23)
------------------

- Fixed argument signature in new class based view. Thanks, mkai.

0.9 (2012-11-21)
----------------

- Deprecated ``ROBOTS_SITEMAP_URL`` setting. Use ``ROBOTS_SITEMAP_URLS``
  instead.

- Refactored ``rule_list`` view to be class based. django-robots now
  requires Django >= 1.3.

- Stop returning 404 pages if there are no Rules setup on the site. Instead
  dissallow access for all robots.

- Added an initial South migration. If you're using South you have to "fake"
  the initial database migration::

     python manage.py migrate --fake robots 0001

- Added initial Sphinx docs.
