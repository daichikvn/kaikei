from django import forms
from .models import Sales


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields =['date', 'total_sales', 'lunch_sales', 'drink_sales', 'dinner_guest', 'lunch_guest', 'bank_deposit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs['placeholder'] = field.label