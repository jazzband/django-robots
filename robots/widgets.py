from django.forms import Select
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.conf import settings
#from django.contrib.admin.widgets import FilteredSelectMultiple
from robots.models import Url


# class CustomDisallowedWidget(FilteredSelectMultiple):

#     def render(self, name, value, attrs=None, choices=()):
#         # value = value or []
#         # admin, _ = Url.objects.get_or_create(pattern='/admin/')
#         # if admin.id not in value:
#         #     value.insert(0, admin.id)
#         return super(CustomDisallowedWidget, self).render(name, value, attrs, choices)


class CustomSitesSelector(Select):

    def value_from_datadict(self, data, files, name):
        return (super(CustomSitesSelector, self).value_from_datadict(data, files, name), )

    def render(self, name, value, attrs=None, choices=()):
        from django.core.urlresolvers import reverse
        value = value[0] if value else value
        output = super(CustomSitesSelector, self).render(name, value, attrs=attrs, choices=choices)
        t = loader.get_template("robots/reload_disallowed.js")
        c = Context({
            'STATIC_URL': settings.STATIC_URL,
            'site_patterns_url': reverse('site_patterns')
        })
        return output + mark_safe(t.render(c))
