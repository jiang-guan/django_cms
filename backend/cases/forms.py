from django import forms
from .models import Case, NaturalPerson, LegalEntity

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description']

class NaturalPersonForm(forms.ModelForm):
    class Meta:
        model = NaturalPerson
        exclude = ['case']

class LegalEntityForm(forms.ModelForm):
    class Meta:
        model = LegalEntity
        exclude = ['case']



