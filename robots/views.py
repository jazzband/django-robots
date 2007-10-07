from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings

from robots.models import Rule

def rules_list(request, template_name='robots/rule_list.html', 
        mimetype='text/plain', status_code=200):
    """
    Returns a generated robots.txt file with correct mimetype (text/plain),
    status code (200 or 404), sitemap url (automatically) and crawl delay 
    (if settings.ROBOTS_CRAWL_DELAY is given).
    """
    protocol = request.is_secure() and 'https' or 'http'
    current_site = Site.objects.get_current()
    try:
        sitemap_url = reverse('django.contrib.sitemaps.views.index')
    except NoReverseMatch:
        try:
            sitemap_url = reverse('django.contrib.sitemaps.views.sitemap')
        except NoReverseMatch:
            sitemap_url = None
    use_sitemap = getattr(settings, 'ROBOTS_USE_SITEMAP', True)
    if sitemap_url is not None and use_sitemap:
        sitemap_url = "%s://%s%s" % (protocol, current_site.domain, sitemap_url)
    rules = Rule.objects.filter(sites=current_site)
    if not rules.count():
        status_code = 404
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'rules': rules,
        'sitemap_url': sitemap_url,
        'crawl_delay': getattr(settings, 'ROBOTS_CRAWL_DELAY', False)
    })
    return HttpResponse(t.render(c), status=status_code, mimetype=mimetype)
