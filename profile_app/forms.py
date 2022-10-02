from django import forms
from core_app import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['name', 'photo', 'cover_photo', 'bio', 'date_of_birth']
