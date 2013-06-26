from django.conf.urls.defaults import *

urlpatterns = patterns('robots.views',
    url(r'^robots.txt$', 'rules_list', name='robots_rule_list'),
    url(r'^robots/site_patterns$', 'site_patterns', name='site_patterns'),
)
