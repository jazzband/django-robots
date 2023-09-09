from django import forms
from django.utils.translation import gettext_lazy as _

from robots.models import Rule


class RuleAdminForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = "__all__"

    def clean(self):
        if not self.cleaned_data.get("disallowed", False) and not self.cleaned_data.get(
            "allowed", False
        ):
            raise forms.ValidationError(
                _("Please specify at least one allowed or disallowed URL.")
            )
        return self.cleaned_data
