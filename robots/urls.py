from django.conf.urls.defaults import *

urlpatterns = patterns('robots.views',
    (r'^$', 'rules_list'),
)
