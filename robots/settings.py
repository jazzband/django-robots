from warnings import warn
from django.conf import settings

#: A list of one or more sitemaps to inform robots about:
SITEMAP_URLS = []
SITEMAP_URLS.extend(getattr(settings, 'ROBOTS_SITEMAP_URLS', []))

#: A list of one or more sitemaps views used to render sitemaps in the current project:
#: The defaults are the ones that come fromm django, but if the users override them
#: we just extend the list. If the urls have no reverse lookup, we won't embed them in the robots
SITEMAP_VIEWS = ['django.contrib.sitemaps.views.index', 'django.contrib.sitemaps.views.sitemap']
SITEMAP_VIEWS.extend(getattr(settings, 'ROBOTS_SITEMAP_VIEWS', []))

# For backwards-compatibility, we'll automatically add a single URL
# to the list:
SITEMAP_URL = getattr(settings, 'ROBOTS_SITEMAP_URL', None)
if SITEMAP_URL is not None:
    warn("The ``SITEMAP_URL`` setting is deprecated. "
         "Use ``SITEMAP_URLS`` instead.", PendingDeprecationWarning)
    SITEMAP_URLS.append(SITEMAP_URL)

USE_SITEMAP = getattr(settings, 'ROBOTS_USE_SITEMAP', True)

CACHE_TIMEOUT = getattr(settings, 'ROBOTS_CACHE_TIMEOUT', None)
