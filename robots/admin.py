from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_text_list

from robots.widgets import CustomSitesSelector
from django.contrib.admin.widgets import FilteredSelectMultiple
from robots.forms import RuleAdminForm
from robots.models import Rule, Url
from robots.helpers import get_url


class RuleAdmin(admin.ModelAdmin):
    form = RuleAdminForm
    fieldsets = (
        (None, {'fields': ('sites', )}),
        (_('URL patterns'), {
            'fields': ('disallowed',),
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('crawl_delay',),
        }),
    )

    list_display = ('site_name', 'site_domain', 'allowed_urls', 'disallowed_urls')
    list_display_links = ('site_name', 'site_domain')
    search_fields = ('sites__name', 'sites__domain')

    def site_name(self, obj):
        return get_text_list([s.name for s in obj.sites.all()], _('and'))
    site_name.short_description = ('Site(s) (Display Name)')

    def site_domain(self, obj):
        return get_text_list([s.domain for s in obj.sites.all()], _('and'))
    site_domain.short_description = 'Site(s)'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super(RuleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'sites':
            #here the sites field will have the queryset attr
            #  based on user (global page)permissions
            field.widget = CustomSitesSelector()
        elif db_field.name == 'disallowed':
            field.widget = FilteredSelectMultiple(verbose_name='Disallows',\
                                                is_stacked=False)
        return field

    def save_model(self, request, obj, form, change):
        super(RuleAdmin, self).save_model(request, obj, form, change)
        all_pattern = get_url('/*')
        obj.allowed.add(all_pattern)


admin.site.register(Url)
admin.site.register(Rule, RuleAdmin)
