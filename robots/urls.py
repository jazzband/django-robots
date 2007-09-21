from django.conf.urls.defaults import *
from django.contrib.sites.models import Site
from django.conf import settings

current_site = Site.objects.get_current()

options = {
    'queryset': current_site.rule_set.all(),
    'allow_empty': True,
    'extra_context': {
        'sitemap_url': getattr(settings, "SITEMAP_URL", False),
        }
}

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', options),
)
