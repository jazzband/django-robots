=======================================
Robots exclusion application for Django
=======================================

This is a basic Django application to manage robots.txt files following the
`robots exclusion standard`_, complementing the Django `Sitemap contrib app`_.

.. _robots exclusion standard: http://www.robotstxt.org/
.. _Sitemap contrib app: http://www.djangoproject.com/documentation/sitemaps/

How to use it in your own django application
============================================

0. Get the source from the application site at::

        http://code.google.com/p/django-robots/

1. Follow the instructions in the INSTALL.txt file

2. Edit the settings.py of your Django project::

    # Add ``robots`` to the ``INSTALLED_APPS`` of your Django project

    # Check if ``django.contrib.sites`` and ``django.contrib.admin`` are in
      ``INSTALLED_APPS`` and add if necessary
      
      It should look something like this::
      
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.admin',
            'django.contrib.flatpages',
            'robots',
            'myproject.myapp',
        )
    
    # Check if ``django.template.loaders.app_directories.load_template_source``
      is in the ``TEMPLATE_LOADERS`` list.

      It should look something like this::

        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.load_template_source',
            'django.template.loaders.app_directories.load_template_source',
        )

3. Add this line to your site's root URLConf::

        (r'^robots.txt$', include('robots.urls')),

4. Sync your database via shell (``manage.py syncdb`` in your project dir).

5. Create ``Rule`` and ``Url`` objects in the admin interface.

6. Go to /robots.txt under the URL of your Django site to see the results.

Usage
=====

The application consists of two database models which are tied together with a
m2m relationship::

    1. ``Rule`` - contains a User Agent field and multiple URL patters to
       define a abstract disallowance rule. Each rule will be rendered with
       all of its related URLs in a simple and plain text file.

       Please have a look at the `database of web robots`_ for a full list of
       existing web robots user agent strings.

    2. ``Url`` - defines a case-sensitive and exact URL pattern which is used
       together with an user agent string to disallow the access for web robots.

You can set ``SITEMAP_URL`` in your projects settings.py file to the URL of your
sitemap.xml file, for example::

    SITEMAP_URL = "http://www.djangoproject.com/sitemap.xml"

This is added to the resulting robots.txt file as a "Sitemap:" statement - very
useful especially in combination with the Django Sitemaps contrib app.

If no rule exists it automatically allows every web robot access to every URL.

.. _database of web robots: http://www.robotstxt.org/wc/active/html/index.html

Bugs, support, questions and headaches
======================================

Please leave your `questions and problems`_ on the `designated Google Code site`_:

.. _designated Google Code site: http://code.google.com/p/django-robots/
.. _questions and problems: http://code.google.com/p/django-robots/issues/list
