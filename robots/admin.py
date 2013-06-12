from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_text_list

from robots.models import Url, Rule
from robots.widgets import CustomSitesSelector, CustomDisallowsSelector
from django.utils.functional import wraps
from django import forms
from django.forms.util import ErrorList
from django.contrib.sites.models import Site


ID_PREFIX = 'disallowed'


class RuleAdmin(admin.ModelAdmin):
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

    def site_name(self, obj):
        return get_text_list([s.name for s in obj.sites.all()], _('and'))
    site_name.short_description = ('Site(s) (Display Name)')

    def site_domain(self, obj):
        return get_text_list([s.domain for s in obj.sites.all()], _('and'))
    site_domain.short_description = 'Site(s)'

    def get_form(self, request, obj=None, **kwargs):
        form = super(RuleAdmin, self).get_form(request, obj)

        def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                     initial=None, error_class=ErrorList, label_suffix=':',
                     empty_permitted=False, instance=None):
            super(self.__class__, self).__init__(data, files, auto_id, prefix,\
                                                 initial, error_class, \
                                                 label_suffix, empty_permitted,\
                                                 instance)
            sites_field = self.fields['sites']
            site_id = self.data.get('sites', instance.sites.all()[0].id if instance else sites_field.choices.queryset[0].id)
            selected_site = Site.objects.get(pk=site_id)
            protocol = 'https' if request.is_secure() else 'http'
            disallowed_field = self.fields['disallowed']
            disallowed_field.choices = get_choices(selected_site, protocol)

        form.__init__ = __init__


        def clean_disallowed(self):
            if not self.cleaned_data.get("disallowed", False):
                raise forms.ValidationError(
                    _('Please specify at least one disallowed URL.'))
            return self.cleaned_data['disallowed']
        form.clean_disallowed = clean_disallowed

        @wraps(form._clean_fields)
        def _clean_fields(self):
            field = self.fields['disallowed']

            #this is a list of ids like ['1', '4', 'disallowed_2', 'disallowed_5', ...]
            # !! Notice the fake ids like 'disallowed_2' and 'disallowed_5'
            selected_values = field.widget.value_from_datadict(self.data, self.files, self.add_prefix('disallowed'))

            # As some of the ids in selected_values for disasalowed urlsd
            #  are not db ids (eg disallowed_2), I need to save in db the
            #  coresponding patterns in order to get real db ids. The fake ids
            #  in selected_values and field.choices will be replaced with the
            #  real ids.
            if selected_values:
                for i, choice in enumerate(field.choices):
                    # choice is a pair like ['id', '/pattern/']
                    if choice[0] in selected_values and choice[0].startswith(ID_PREFIX):
                        url = Url.objects.create(pattern=choice[1])
                        selected_values[selected_values.index(choice[0])] = str(url.id)
                        field.choices[i][0] = str(url.id)

            # Here all the ids for disallowed selected_values have real db ids,
            #  so calling super(...)._clean_fields() will not throw Validation
            #  error for the selected disallowed patterns
            super(self.__class__, self)._clean_fields()
        form._clean_fields = _clean_fields

        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super(RuleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'sites':
            #here the sites field will have the queryset attr
            #  based on user (global)permissions
            field.widget = CustomSitesSelector()
        elif db_field.name == 'disallowed':
            field.widget = CustomDisallowsSelector(verbose_name='Disallows',\
                                                is_stacked=False)
        return field


def get_choices(site, protocol):
    """
    Returns a list with the urls patterns for the site parameter
    The list will be in this format required by the disallowed field widget:
    [['1', '/pattern1/'], ['2', '/pattern2/'], ['disallowed_3', '/pattern4/'], ...]

    The patterns are taken from the sitemap for the site param.
    Some of the ids are real db ids, and others may be fake ones
    (generated here).
    """
    from cms.sitemaps.cms_sitemap import CMSSitemap
    from django.conf import settings

    settings.__class__.SITE_ID.value = site.id
    admin, _ = Url.objects.get_or_create(pattern='/admin/')

    #generate patterns from the sitemap
    urls = CMSSitemap().get_urls(site=site, protocol=protocol)
    all_patterns = map(lambda item: item['location'].replace("%s://%s" % (protocol, site.domain), ''), urls)

    #some patterns are already present in the db and I need their real ids
    db_urls = Url.objects.filter(pattern__in=all_patterns).values_list('id', 'pattern')
    db_ids, db_patterns = ([], []) if not db_urls.exists() else zip(*db_urls)

    # Generate some fake ids for the patterns that were not
    #  previously saved in the db
    remaining_patterns = [x for x in all_patterns if x not in db_patterns]
    fake_ids = map(lambda x: '%s_%d' % (ID_PREFIX, x), range(len(remaining_patterns)))

    # Make sure that the '/admin/' pattern is allways present
    #  in the choice list
    admin_pair = [[str(admin.id), admin.pattern]]

    # returns a list of ['id', 'pattern'] pairs
    return admin_pair + \
        map(lambda x: [x[0], x[1]], zip(db_ids, db_patterns)) + \
        map(lambda x: [x[0], x[1]], zip(fake_ids, remaining_patterns))



admin.site.register(Url)
admin.site.register(Rule, RuleAdmin)
