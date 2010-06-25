from django.conf import settings

#: A list of one or more sitemaps to inform robots about:
SITEMAP_URLS = []
SITEMAP_URLS.extend(getattr(settings,'ROBOTS_SITEMAP_URLS', []))

# For backwards-compatibility, we'll automatically add a single URL
# to the list:
if hasattr(settings, 'ROBOTS_SITEMAP_URL'):
    SITEMAP_URLS.append(settings.ROBOTS_SITEMAP_URL)

USE_SITEMAP = getattr(settings, 'ROBOTS_USE_SITEMAP', True)

CACHE_TIMEOUT = getattr(settings, 'ROBOTS_CACHE_TIMEOUT', None)
