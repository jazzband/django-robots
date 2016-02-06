
Changelog
=========

2.0 (unreleased)
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
