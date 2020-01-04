from django.conf.urls import url
from robots.views import rules_list

urlpatterns = [
    url(r"^$", rules_list, name="robots_rule_list"),
]
