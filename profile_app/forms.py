from django import forms
from core_app import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['name', 'photo', 'cover_photo', 'bio', 'date_of_birth']

class UpdateProfileForm(forms.Form):
    name = forms.CharField(max_length=20, required=False)
    photo = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(required=False)

