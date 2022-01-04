=======================================
Robots exclusion application for Django
=======================================

.. include:: ../README.rst

Contents:

.. toctree::
   :maxdepth: 2

   history


Installation
============

Use your favorite Python installer to install it from PyPI::

    pip install django-robots

Or get the source from the application site at::

    http://github.com/jazzband/django-robots/

To install the sitemap app, then follow these steps:

1. Add ``'robots'`` to your INSTALLED_APPS_ setting.
2. Make sure ``'django.template.loaders.app_directories.Loader'``
   is in your TEMPLATES setting. It's in there by default, so
   you'll only need to change this if you've changed that setting.
3. Make sure you've installed the `sites framework`_.
4. Run the ``migrate`` management command

.. _INSTALLED_APPS: http://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
.. _TEMPLATES: https://docs.djangoproject.com/en/dev/ref/settings/#templates
.. _sites framework: http://docs.djangoproject.com/en/dev/ref/contrib/sites/

Sitemaps
--------

By default a ``Sitemap`` statement is automatically added to the resulting
robots.txt by reverse matching the URL of the installed `Sitemap contrib app`_.
This is especially useful if you allow every robot to access your whole site,
since it then gets URLs explicitly instead of searching every link.

To change the default behaviour to omit the inclusion of a sitemap link,
change the ``ROBOTS_USE_SITEMAP`` setting in your Django settings file to::

    ROBOTS_USE_SITEMAP = False

In case you want to use specific sitemap URLs instead of the one that is
automatically discovered, change the ``ROBOTS_SITEMAP_URLS`` setting to::

    ROBOTS_SITEMAP_URLS = [
        'http://www.example.com/sitemap.xml',
    ]

If the sitemap is wrapped in a decorator, dotted path reverse to discover
the sitemap URL does not work.
To overcome this, provide a name to the sitemap instance in ``urls.py``::

    urlpatterns = [
        ...
        re_path(r'^sitemap.xml$', cache_page(60)(sitemap_view), {'sitemaps': [...]}, name='cached-sitemap'),
        ...
    ]

and inform django-robots about the view name by adding the followin setting::

    ROBOTS_SITEMAP_VIEW_NAME = 'cached-sitemap'


.. _Sitemap contrib app: http://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/

Use ``ROBOTS_SITEMAP_VIEW_NAME`` also if you use custom sitemap views (e.g.: wagtail custom sitemaps).

Initialization
==============

To activate robots.txt generation on your Django site, add this line to your
URLconf_::

    re_path(r'^robots\.txt', include('robots.urls')),

This tells Django to build a robots.txt when a robot accesses ``/robots.txt``.
Then, please sync your database to create the necessary tables and create
``Rule`` objects in the admin interface or via the shell.

.. _URLconf: http://docs.djangoproject.com/en/dev/topics/http/urls/
.. _sync your database: http://docs.djangoproject.com/en/dev/ref/django-admin/#syncdb

Rules
=====

``Rule`` - defines an abstract rule which is used to respond to crawling web
robots, using the `robots exclusion protocol`_, a.k.a. robots.txt.

You can link multiple URL pattern to allows or disallows the robot identified
by its user agent to access the given URLs.

The crawl delay field is supported by some search engines and defines the
delay between successive crawler accesses in seconds. If the crawler rate is a
problem for your server, you can set the delay up to 5 or 10 or a comfortable
value for your server, but it's suggested to start with small values (0.5-1),
and increase as needed to an acceptable value for your server. Larger delay
values add more delay between successive crawl accesses and decrease the
maximum crawl rate to your web server.

The `sites framework`_ is used to enable multiple robots.txt per Django instance.
If no rule exists it automatically allows every web robot access to every URL.

Please have a look at the `database of web robots`_ for a full list of
existing web robots user agent strings.

.. _robots exclusion protocol: http://en.wikipedia.org/wiki/Robots_exclusion_standard
.. _'sites' framework: http://www.djangoproject.com/documentation/sites/
.. _database of web robots: http://www.robotstxt.org/db.html

Host directive
==============
By default a ``Host`` statement is automatically added to the resulting
robots.txt to avoid mirrors and select the main website properly.

To change the default behaviour to omit the inclusion of host directive,
change the ``ROBOTS_USE_HOST`` setting in your Django settings file to::

    ROBOTS_USE_HOST = False

if you want to prefix the domain with the current request protocol
(**http** or **https** as in ``Host: https://www.mysite.com``) add this setting::

    ROBOTS_USE_SCHEME_IN_HOST = True

URLs
====

``Url`` - defines a case-sensitive and exact URL pattern which is used to
allow or disallow the access for web robots. Case-sensitive.

A missing trailing slash does also match files which start with the name of
the given pattern, e.g., ``'/admin'`` matches ``/admin.html`` too.

Some major search engines allow an asterisk (``*``) as a wildcard to match any
sequence of characters and a dollar sign (``$``) to match the end of the URL,
e.g., ``'/*.jpg$'`` can be used to match all jpeg files.

Caching
=======

You can optionally cache the generation of the ``robots.txt``. Add or change
the ``ROBOTS_CACHE_TIMEOUT`` setting with a value in seconds in your Django
settings file::

    ROBOTS_CACHE_TIMEOUT = 60*60*24

This tells Django to cache the ``robots.txt`` for 24 hours (86400 seconds).
The default value is ``None`` (no caching).

Bugs and feature requests
=========================

As always your mileage may vary, so please don't hesitate to send feature
requests and bug reports:

    https://github.com/jazzband/django-robots/issues
