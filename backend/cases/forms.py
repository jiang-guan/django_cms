from django import forms
from .models import Case, NaturalPerson, LegalEntity, UserProfile

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class NaturalPersonForm(forms.ModelForm):
    class Meta:
        model = NaturalPerson
        exclude = ['case']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class LegalEntityForm(forms.ModelForm):
    class Meta:
        model = LegalEntity
        exclude = ['case']

class CaseReviewForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['status', 'rejection_reason']
        widgets = {
            'rejection_reason': forms.Textarea(attrs={'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'office']



