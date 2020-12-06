import sys

from django import forms

from robots.models import Rule

if sys.version_info[0] == 2:
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class RuleAdminForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = "__all__"

    def clean(self):
        if not self.cleaned_data.get("disallowed", False) and not self.cleaned_data.get(
            "allowed", False
        ):
            raise forms.ValidationError(
                _("Please specify at least one allowed or dissallowed URL.")
            )
        return self.cleaned_data
