from django.http import HttpResponse
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import loader, RequestContext
from django.views.decorators.cache import cache_page

from django.contrib.sites.models import Site

from robots.models import Rule
from robots import settings

def rules_list(request, template_name='robots/rule_list.html',
        mimetype='text/plain', status_code=200):
    """
    Returns a generated robots.txt file with correct mimetype (text/plain),
    status code (200 or 404), sitemap url (automatically).
    """
    scheme = request.is_secure() and 'https' or 'http'
    current_site = Site.objects.get_current()
    if settings.SITEMAP_URL:
        sitemap_url = settings.SITEMAP_URL
    else:
        try:
            sitemap_url = reverse('django.contrib.sitemaps.views.index')
        except NoReverseMatch:
            try:
                sitemap_url = reverse('django.contrib.sitemaps.views.sitemap')
            except NoReverseMatch:
                sitemap_url = None
    if sitemap_url is not None and settings.USE_SITEMAP:
        sitemap_url = "%s://%s%s" % (scheme, current_site.domain, sitemap_url)
    rules = Rule.objects.filter(sites=current_site)
    if not rules.count() and sitemap_url is None:
        status_code = 404
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'rules': rules,
        'sitemap_url': sitemap_url,
    })
    return HttpResponse(t.render(c), status=status_code, mimetype=mimetype)

if settings.CACHE_TIMEOUT:
    rules_list = cache_page(rules_list, settings.CACHE_TIMEOUT)
