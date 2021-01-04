from django import forms
from .models import Cost


class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields =['date', 'shop', 'price', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs['placeholder'] = field.label