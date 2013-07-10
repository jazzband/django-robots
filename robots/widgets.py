from django.forms import Select
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from robots.models import Url
from django.contrib.admin.templatetags.admin_static import static
from django.utils.translation import ugettext as _
from django.core.urlresolvers import NoReverseMatch


class CustomDisallowedWidget(FilteredSelectMultiple):

    # def __init__(self, verbose_name, is_stacked):
    #     super(CustomDisallowedWidget ,self).__init__(verbose_name, is_stacked)

    def render(self, name, value, attrs=None, choices=()):
        output = [super(CustomDisallowedWidget, self).render(name, value, attrs, choices)]

        info = (Url._meta.app_label, Url._meta.object_name.lower())
        if not Url in admin.site._registry:
            try:
                related_url = reverse('admin:%s_%s_adds' % info, current_app=admin.site.name)
                output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> '  % (related_url, 'disallowed'))
                output.append(u'<img src="%s" width="10" height="10" alt="%s"/></a>'
                      % (static('admin/img/icon_addlink.gif'), _('Add Another')))
            except NoReverseMatch:
                pass

        return mark_safe(u''.join(output))


class CustomSitesSelector(Select):

    def value_from_datadict(self, data, files, name):
        # the sites filed expects a list of values, while this widget returns
        # one by default
        return (super(CustomSitesSelector, self).value_from_datadict(data, files, name), )

    def render(self, name, value, attrs=None, choices=()):
        output = super(CustomSitesSelector, self).render(name, value, attrs=attrs, choices=choices)

        template = loader.get_template("robots/sites_selector.html")
        context = Context({
            'select_widget_output' : output,
            'STATIC_URL': settings.STATIC_URL,
            'site_patterns_url': reverse('site_patterns')
        })
        return mark_safe(template.render(context))
