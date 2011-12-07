from warnings import warn
from django.conf import settings

#: A list of one or more sitemaps to inform robots about:
SITEMAP_URLS = []
SITEMAP_URLS.extend(getattr(settings, 'ROBOTS_SITEMAP_URLS', []))

# For backwards-compatibility, we'll automatically add a single URL
# to the list:
SITEMAP_URL = getattr(settings, 'ROBOTS_SITEMAP_URL', None)
if SITEMAP_URL is not None:
    warn("The ``SITEMAP_URL`` setting is deprecated. "
         "Use ``SITEMAP_URLS`` instead.", PendingDeprecationWarning)
    SITEMAP_URLS.append(SITEMAP_URL)

USE_SITEMAP = getattr(settings, 'ROBOTS_USE_SITEMAP', True)

CACHE_TIMEOUT = getattr(settings, 'ROBOTS_CACHE_TIMEOUT', None)
