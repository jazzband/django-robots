from django import forms
from django.utils.translation import ugettext_lazy as _
from robots.models import Rule, Url
from django.contrib.sites.models import Site
from robots.helpers import ID_PREFIX, get_site_id, get_choices
from robots.settings import ADMIN


class RuleAdminForm(forms.ModelForm):
    class Meta:
        model = Rule

    ERR_EMPTY_DISALLOWED = _('Please specify at least one disallowed URL.')
    ERR_ADMIN_IN_DISALLOWED = _('/admin/ pattern must be disallowed by default. Please select it in the chosen list.')

    def __init__(self, *args, **kwargs):
        super(RuleAdminForm, self).__init__(*args, **kwargs)
        site_id = get_site_id(self.data, self.instance, self.fields['sites'])
        self._initialize_sites_field(site_id)
        self._initialize_disallowed_field(site_id)

    def _initialize_sites_field(self, site_id):
        sites_field = self.fields['sites']
        qs = sites_field.queryset
        if self._is_new_rule():
            # new rules can only be set for sites with rule=null
            qs = qs.filter(rule__isnull=True)
        else:
            # The site for existing rules cannot be changed
            qs = qs.filter(pk=site_id)
        sites_field.queryset = qs

    def _initialize_disallowed_field(self, site_id):
        selected_site = Site.objects.get(pk=site_id)
        disallowed_field = self.fields['disallowed']
        disallowed_field.choices = get_choices(selected_site, 'http')
        if self._is_new_rule():
            #/admin/ pattern is allways default
            admin_id = self._get_admin_id(disallowed_field.choices) or ''
            self.initial = {'disallowed': [admin_id]}

    def _get_admin_id(self, choices):
        return next((c[0] for c in choices if c[1] == ADMIN), None)

    def _is_new_rule(self):
        return self.instance and not self.instance.id

    def clean_disallowed(self):
        if not self.cleaned_data.get("disallowed", False):
            raise forms.ValidationError(self.ERR_EMPTY_DISALLOWED)
        self._check_admin_is_present()
        return self.cleaned_data['disallowed']

    def _check_admin_is_present(self):
        field = self.fields['disallowed']
        selected_values = field.widget.value_from_datadict(self.data, self.files, self.add_prefix('disallowed'))
        admin_id = self._get_admin_id(field.choices)
        if str(admin_id) not in selected_values:
            raise forms.ValidationError(self.ERR_ADMIN_IN_DISALLOWED)

    def _clean_fields(self):
        field = self.fields['disallowed']

        #this is a list of ids like ['1', '4', 'disallowed_2', 'disallowed_5', ...]
        # !! Notice the fake ids like 'disallowed_2' and 'disallowed_5'
        # (see robots.helpers.get_choices(...))
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
