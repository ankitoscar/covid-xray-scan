from django import forms
from .models import Patient


class ImageForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name','scan')