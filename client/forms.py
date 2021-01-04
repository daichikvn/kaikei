from django import forms
from .models import Client, Visit


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'receipt_name', 'tel_number', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs['placeholder'] = field.label


class VisitCreateForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('visit_date', 'menu')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs['placeholder'] = field.label