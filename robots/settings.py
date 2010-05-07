from django.conf import settings


SITEMAP_URL = getattr(settings,'ROBOTS_SITEMAP_URL', None)

USE_SITEMAP = getattr(settings, 'ROBOTS_USE_SITEMAP', True)

CACHE_TIMEOUT = getattr(settings, 'ROBOTS_CACHE_TIMEOUT', None)
