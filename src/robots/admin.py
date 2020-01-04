from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from robots.forms import RuleAdminForm
from robots.models import Rule, Url


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
