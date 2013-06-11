from django import forms
from django.utils.translation import ugettext_lazy as _

from robots.models import Rule, Url
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField
from django.contrib.sites.models import Site
from cms.sitemaps import CMSSitemap
from django.forms import Select
from django.forms.widgets import HiddenInput

class SitesChoice(ModelMultipleChoiceField):

    def clean(self, value):
        value = (value, )
        return super(SitesChoice, self).clean(value)


class RuleAdminForm(forms.ModelForm):
    class Meta:
        model = Rule

    sites = SitesChoice(
        queryset=Site.objects.all(),
        required=False,
#        widget=Select()
        widget=FilteredSelectMultiple(verbose_name='Sites', is_stacked=False)
    )

    # from django.contrib.sites.models import get_current_site
    #  {'sitemaps': {'cmspages': CMSSitemap}}

    # disallowed = ModelChoiceField(
    #     queryset=Url.objects.filter(),
    #     required=False,
    #     widget=Select(),
    #     initial=[]
    # )

    def __init__(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        super(RuleAdminForm, self).__init__(*args, **kwargs)
        self.request =request


    def clean(self):
        if not self.cleaned_data.get("disallowed", False):
            raise forms.ValidationError(
                _('Please specify at least one dissallowed URL.'))
        return self.cleaned_data

