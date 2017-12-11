# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django
import django.contrib.sitemaps.views
import django.views.i18n
import django.views.static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.decorators.cache import cache_page

if django.VERSION[:2] >= (2, 0):
    from django.urls import include, re_path as url
else:
    from django.conf.urls import include, url

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^admin/', admin.site.urls),  # NOQA
    url(r'^/', include('robots.urls')),  # NOQA
    url(r'^sitemap.xml$', sitemap_view, {'sitemaps': []}),
    url(r'^other/sitemap.xml$', cache_page(60)(sitemap_view), {'sitemaps': []}, name='cached-sitemap'),
]
