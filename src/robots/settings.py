from django.conf import settings

SITEMAP_URLS = getattr(settings, "ROBOTS_SITEMAP_URLS", [])
USE_SITEMAP = getattr(settings, "ROBOTS_USE_SITEMAP", True)
USE_HOST = getattr(settings, "ROBOTS_USE_HOST", True)
CACHE_TIMEOUT = getattr(settings, "ROBOTS_CACHE_TIMEOUT", None)
SITE_BY_REQUEST = getattr(settings, "ROBOTS_SITE_BY_REQUEST", False)
USE_SCHEME_IN_HOST = getattr(settings, "ROBOTS_USE_SCHEME_IN_HOST", False)
SITEMAP_VIEW_NAME = getattr(settings, "ROBOTS_SITEMAP_VIEW_NAME", False)
