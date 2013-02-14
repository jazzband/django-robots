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
    # the shallow clone of the list ensures we don't alter the settings.SITEMAp_URLS
    sitemap_urls = settings.SITEMAP_URLS[:]
    sitemap_views = settings.SITEMAP_VIEWS

    if not sitemap_urls and settings.USE_SITEMAP:
        sitemap_url = None
        
        for sitemap_view in sitemap_views:
            try:
                sitemap_slug = reverse(sitemap_view)
                if sitemap_slug is not None:
                    sitemap_urls.append("%s://%s%s" % (scheme, current_site.domain, sitemap_slug))
            except NoReverseMatch:
                pass

    rules = Rule.objects.filter(sites=current_site)

    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'rules': rules,
        'sitemap_url': sitemap_url, # for old templates
        'sitemap_urls': sitemap_urls,
    })
    return HttpResponse(t.render(c), status=status_code, mimetype=mimetype)

if settings.CACHE_TIMEOUT:
    rules_list = cache_page(rules_list, settings.CACHE_TIMEOUT)
