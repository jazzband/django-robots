import sys

from django.contrib import admin

from robots.forms import RuleAdminForm
from robots.models import Rule, Url

if sys.version_info[0] == 2:
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class RuleAdmin(admin.ModelAdmin):
    form = RuleAdminForm
    fieldsets = (
        (None, {"fields": ("robot", "sites")}),
        (_("URL patterns"), {"fields": ("allowed", "disallowed")}),
        (
            _("Advanced options"),
            {"classes": ("collapse",), "fields": ("crawl_delay",)},
        ),
    )
    list_filter = ("sites",)
    list_display = ("robot", "allowed_urls", "disallowed_urls")
    search_fields = ("robot", "allowed__pattern", "disallowed__pattern")
    filter_horizontal = ("sites", "allowed", "disallowed")


admin.site.register(Url)
admin.site.register(Rule, RuleAdmin)
