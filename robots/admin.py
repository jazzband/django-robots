from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_text_list

from robots.models import Url, Rule
from robots.forms import RuleAdminForm
from django.forms import Select
from django.contrib.admin.widgets import FilteredSelectMultiple
#from django.utils.functional import wraps
from django import forms

ID_PREFIX = 'disallowed'

class RuleAdmin(admin.ModelAdmin):
#    form = RuleAdminForm
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

    list_filter = ('sites',)
    list_display = ('site_name', 'site_domain', 'disallowed_urls')
    list_display_links = ('site_name', 'site_domain')
    search_fields = ('sites__name', 'sites__domain')

    def get_form(self, request, obj=None, **kwargs):
        form = super(RuleAdmin, self).get_form(request, obj)

        def clean_disallowed(self):
            if not self.cleaned_data.get("disallowed", False):
                raise forms.ValidationError(
                    _('Please specify at least one dissallowed URL.'))
            return self.cleaned_data['disallowed']

        def _clean_fields(self):
            field = self.fields['disallowed']
            selected_values = field.widget.value_from_datadict(self.data, self.files, self.add_prefix('disallowed'))

            # As some of the ids in selected_values for disasalowed urls are not db ids (eg disallowed_2),
            # I need to save in db the coresponding patterns in order to get real db ids.
            # The fake ids in selected_values and field.choices will be replaced with the real ids.
            if selected_values:
                for i , f in enumerate(field.choices):
                    if f[0] in selected_values and f[0].startswith(ID_PREFIX):
                        url = Url.objects.get_or_create(pattern=f[1])
                        selected_values[selected_values.index(f[0])] = str(url.id)
                        field.choices[i][0] = str(url.id)

            # Here all the ids for disallowed selected_values have real db ids,
            # so calling super(..)._clean_fields(...) will not throw Validation error
            # for the selected dosallowed patterns
            super(self.__class__, self)._clean_fields()

        form.clean_disallowed = clean_disallowed
        form._clean_fields = _clean_fields

        sites_field = form.base_fields['sites']
        disallowed_field = form.base_fields['disallowed']
        set_disallowed_choices(sites_field, disallowed_field, obj, 'https' if request.is_secure() else 'http')

        return form

    def site_name(self, obj):
        return get_text_list([s.name for s in obj.sites.all()], _('and'))
    site_name.short_description = ('Site(s) (Display Name)')

    def site_domain(self, obj):
        return get_text_list([s.domain for s in obj.sites.all()], _('and'))
    site_domain.short_description = 'Site(s)'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        ff = super(RuleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'sites':
            ff.widget = CustomSitesSelector()
        elif db_field.name == 'disallowed':
            ff.widget = CustomDisallowsSelector(verbose_name='Disallows',\
                                                is_stacked=False)
        return ff


class CustomDisallowsSelector(FilteredSelectMultiple):

    def __init__(self, verbose_name, is_stacked):
        super(CustomDisallowsSelector, self).__init__(verbose_name=verbose_name, \
                                                      is_stacked=is_stacked)


class CustomSitesSelector(Select):

    def value_from_datadict(self, data, files, name):
        return (super(CustomSitesSelector, self).value_from_datadict(data, files, name), )

    def render(self, name, value, attrs=None, choices=()):
        value = value[0] if value else value
        return super(CustomSitesSelector, self).render(name, value, attrs, self.choices)


def set_disallowed_choices(sites_field, disallowed_field, obj, protocol):
    selected_site = get_selected_site(obj, sites_field)
    disallowed_field.choices = get_choices(selected_site, protocol)


def get_choices(site, protocol):
    """
    Returns a list with the urls patterns for the site parameter
    The list will be in this format required by the disallowed field widget:
    [['1', '/pattern1/'], ['2', '/pattern2/'], ['disallowed_3', '/pattern4/'], ...]

    The patterns are taken from the sitemap for the site param.
    Some of the ids are real db ids, and others may be fake ones.
    """
    from cms.sitemaps.cms_sitemap import CMSSitemap
    from django.conf import settings

    settings.__class__.SITE_ID.value = site.id
    admin = Url.objects.get_or_create(pattern='/admin/')[0]

    urls = CMSSitemap().get_urls(site=site, protocol=protocol)
    all_patterns = map(lambda item: item['location'].replace("%s://%s" % (protocol, site.domain), ''), urls)

    common_ids, common_patterns = zip(*Url.objects.filter(pattern__in=all_patterns).values_list('id', 'pattern'))

    remaining_patterns = [x for x in all_patterns if x not in common_patterns]
    fake_ids = ['%s_%d' % (ID_PREFIX, i) for i in range(len(remaining_patterns))]

    admin_pair = [[str(admin.id), admin.pattern]]

    return admin_pair + map(lambda x: [x[0], x[1]], zip(common_ids, common_patterns)) +\
        map(lambda x: [x[0], x[1]], zip(fake_ids, remaining_patterns))


def get_selected_site(obj, sites_field):
    if obj:
        return obj.sites.all()[0]
    return sites_field.choices.queryset[0]

admin.site.register(Url)
admin.site.register(Rule, RuleAdmin)
