# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),  # NOQA
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^/', include('robots.urls')),  # NOQA
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': []}),
]
