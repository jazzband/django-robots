from django import forms
from django.utils.translation import ugettext_lazy as _
from robots.models import Rule, Url
from django.contrib.sites.models import Site
from django.forms import Select
from django.forms.widgets import HiddenInput
from robots.helpers import ID_PREFIX, get_site_id, get_choices


class RuleAdminForm(forms.ModelForm):
    class Meta:
        model = Rule

    ERR_NEW_RULE_EXISTING_SITE = _('Cannot assign rule to site %s. It already has a rule assigned.')
    ERR_NEW_SITE_EXISTING_RULE = _('Cannot assign another site to existing rule. Please create a new rule for the site %s if it hasn\'t one.')
    ERR_EMPTY_DISALLOWED = _('Please specify at least one disallowed URL.')
    ERR_ADMIN_IN_DISALLOWED = _('/admin/ pattern is disallowed by default. Please select it in the chosen list.')

    def __init__(self, *args, **kwargs):
        super(RuleAdminForm, self).__init__(*args, **kwargs)
        site_id = get_site_id(self.data, self.instance, self.fields['sites'])
        selected_site = Site.objects.get(pk=site_id)
        disallowed_field = self.fields['disallowed']
        disallowed_field.choices = get_choices(selected_site, 'http')

    def _is_new_rule(self):
        return self.instance and not self.instance.id

    def _check_new_rule_existing_site(self, site):
        if self._is_new_rule() and site.rule_set.all().exists():
            raise forms.ValidationError(self.ERR_NEW_RULE_EXISTING_SITE % site.domain)

    def _check_new_site_existing_rule(self, site):
        if not self._is_new_rule():
            rule_sites_q = self.instance.sites.all()
            rule_site = rule_sites_q[0] if rule_sites_q.exists() else None
            if site != rule_site:
                raise forms.ValidationError(self.ERR_NEW_SITE_EXISTING_RULE % site.domain)

    def _check_admin_is_present(self):
        field = self.fields['disallowed']
        selected_values = field.widget.value_from_datadict(self.data, self.files, self.add_prefix('disallowed'))
        pattern_list = Url.objects.filter(id__in=selected_values).values_list('pattern', flat=True)
        if '/admin/' not in pattern_list:
            raise forms.ValidationError(self.ERR_ADMIN_IN_DISALLOWED)

    def clean_sites(self):
        site_id = self.cleaned_data.get("sites", False)
        if site_id:
            site = Site.objects.get(pk=site_id)
            self._check_new_rule_existing_site(site)
            self._check_new_site_existing_rule(site)
        else:
            raise forms.ValidationError(_('Request improperly configured.'))
        return self.cleaned_data['sites']

    def clean_disallowed(self):
        if not self.cleaned_data.get("disallowed", False):
            raise forms.ValidationError(self.ERR_EMPTY_DISALLOWED)
        self._check_admin_is_present()
        return self.cleaned_data['disallowed']

    def _clean_fields(self):
        field = self.fields['disallowed']

        #this is a list of ids like ['1', '4', 'disallowed_2', 'disallowed_5', ...]
        # !! Notice the fake ids like 'disallowed_2' and 'disallowed_5'
        selected_values = field.widget.value_from_datadict(self.data, self.files, self.add_prefix('disallowed'))

        # As some of the ids in selected_values for disallowed urls
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
        super(RuleAdminForm, self)._clean_fields()
