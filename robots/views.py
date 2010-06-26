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

    sitemap_url = settings.SITEMAP_URL
    sitemap_urls = settings.SITEMAP_URLS

    if not sitemap_urls and settings.USE_SITEMAP:
        sitemap_url = None

        try:
            sitemap_url = reverse('django.contrib.sitemaps.views.index')
        except NoReverseMatch:
            try:
                sitemap_url = reverse('django.contrib.sitemaps.views.sitemap')
            except NoReverseMatch:
                pass

        if sitemap_url is not None:
            sitemap_url = "%s://%s%s" % (scheme, current_site.domain, sitemap_url)
            sitemap_urls.append(sitemap_url)

    rules = Rule.objects.filter(sites=current_site)

    if not rules.count() and not sitemap_urls:
        status_code = 404

    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'rules': rules,
        'sitemap_url': sitemap_url, # for old templates
        'sitemap_urls': sitemap_urls,
    })
    return HttpResponse(t.render(c), status=status_code, mimetype=mimetype)

if settings.CACHE_TIMEOUT:
    rules_list = cache_page(rules_list, settings.CACHE_TIMEOUT)
