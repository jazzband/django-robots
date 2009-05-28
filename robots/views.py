from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.views.decorators.cache import cache_page

from robots.models import Rule

USE_SITEMAP = getattr(settings, 'ROBOTS_USE_SITEMAP', True)
SITEMAP_URL = getattr(settings,'ROBOTS_SITEMAP_URL', None)

def rules_list(request, template_name='robots/rule_list.html', 
        mimetype='text/plain', status_code=200):
    """
    Returns a generated robots.txt file with correct mimetype (text/plain),
    status code (200 or 404), sitemap url (automatically).
    """
    scheme = request.is_secure() and 'https' or 'http'
    current_site = Site.objects.get_current()
    if SITEMAP_URL:
        sitemap_url = SITEMAP_URL
    else:
        try:
            sitemap_url = reverse('django.contrib.sitemaps.views.index')
        except NoReverseMatch:
            try:
                sitemap_url = reverse('django.contrib.sitemaps.views.sitemap')
            except NoReverseMatch:
                sitemap_url = None
    if sitemap_url is not None and USE_SITEMAP:
        sitemap_url = "%s://%s%s" % (scheme, current_site.domain, sitemap_url)
    rules = Rule.objects.filter(sites=current_site)
    if not rules.count():
        status_code = 404
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'rules': rules,
        'sitemap_url': sitemap_url,
    })
    return HttpResponse(t.render(c), status=status_code, mimetype=mimetype)

ROBOTS_CACHE_TIMEOUT = getattr(settings, 'ROBOTS_CACHE_TIMEOUT', None)
if ROBOTS_CACHE_TIMEOUT:
    rules_list = cache_page(rules_list, ROBOTS_CACHE_TIMEOUT)
