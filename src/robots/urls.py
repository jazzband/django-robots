from django.urls import path

from robots.views import rules_list

urlpatterns = [
    path("", rules_list, name="robots_rule_list"),
]
