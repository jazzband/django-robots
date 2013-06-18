from django.forms import Select
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.conf import settings
from django.core.urlresolvers import reverse


class CustomSitesSelector(Select):

    def value_from_datadict(self, data, files, name):
        # the sites filed expects a list of values, while this widget returns
        # one by default
        return (super(CustomSitesSelector, self).value_from_datadict(data, files, name), )

    def render(self, name, value, attrs=None, choices=()):
        output = super(CustomSitesSelector, self).render(name, value, attrs=attrs, choices=choices)
        t = loader.get_template("robots/reload_disallowed.js")
        c = Context({
            'STATIC_URL': settings.STATIC_URL,
            'site_patterns_url': reverse('site_patterns')
        })
        _filter = """<img src="/s/admin/img/selector-search.gif" class="help-tooltip" style="margin-bottom:10px;" alt="" title="Type into this box to filter down the list of available Sites.">
        <input type="text" placeholder="Filter" id="id_sites_input" style="margin-bottom:10px; width: 188px">"""

        return '<div style="float: left;">' + mark_safe(_filter) + '<br>' + output + mark_safe(t.render(c)) + '</div>'
