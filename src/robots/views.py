import django
from django.contrib.sitemaps import views as sitemap_views
from django.contrib.sites.models import Site
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from robots import settings
from robots.models import Rule

if django.VERSION[:2] >= (2, 0):
    from django.urls import NoReverseMatch, reverse
else:
    from django.core.urlresolvers import NoReverseMatch, reverse


class RuleList(ListView):
    """
    Returns a generated robots.txt file with correct mimetype (text/plain),
    status code (200 or 404), sitemap url (automatically).
    """

    model = Rule
    context_object_name = "rules"
    cache_timeout = settings.CACHE_TIMEOUT

    def get_current_site(self, request):
        if settings.SITE_BY_REQUEST:
            return Site.objects.get(domain=request.get_host())
        else:
            return Site.objects.get_current()

    def reverse_sitemap_url(self):
        try:
            if settings.SITEMAP_VIEW_NAME:
                return reverse(settings.SITEMAP_VIEW_NAME)
            else:
                return reverse(sitemap_views.index)
        except NoReverseMatch:
            try:
                return reverse(sitemap_views.sitemap)
            except NoReverseMatch:
                pass

    def get_domain(self):
        scheme = self.request.is_secure() and "https" or "http"
        if not self.current_site.domain.startswith(("http", "https")):
            return "%s://%s" % (scheme, self.current_site.domain)
        return self.current_site.domain

    def get_sitemap_urls(self):
        sitemap_urls = list(settings.SITEMAP_URLS)

        if not sitemap_urls and settings.USE_SITEMAP:
            sitemap_url = self.reverse_sitemap_url()

            if sitemap_url is not None:
                if not sitemap_url.startswith(("http", "https")):
                    sitemap_url = "%s%s" % (self.get_domain(), sitemap_url)
                if sitemap_url not in sitemap_urls:
                    sitemap_urls.append(sitemap_url)

        return sitemap_urls

    def get_queryset(self):
        return Rule.objects.filter(sites=self.current_site)

    def get_context_data(self, **kwargs):
        context = super(RuleList, self).get_context_data(**kwargs)
        context["sitemap_urls"] = self.get_sitemap_urls()
        if settings.USE_HOST:
            if settings.USE_SCHEME_IN_HOST:
                context["host"] = self.get_domain()
            else:
                context["host"] = self.current_site.domain
        else:
            context["host"] = None
        return context

    def render_to_response(self, context, **kwargs):
        return super(RuleList, self).render_to_response(
            context, content_type="text/plain", **kwargs
        )

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, request, *args, **kwargs):
        cache_timeout = self.get_cache_timeout()
        self.current_site = self.get_current_site(request)
        super_dispatch = super(RuleList, self).dispatch
        if not cache_timeout:
            return super_dispatch(request, *args, **kwargs)
        key_prefix = self.current_site.domain
        cache_decorator = cache_page(cache_timeout, key_prefix=key_prefix)
        return cache_decorator(super_dispatch)(request, *args, **kwargs)


rules_list = RuleList.as_view()
