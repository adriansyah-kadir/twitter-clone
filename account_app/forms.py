from django import forms
from core_app import models


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["username", "password", "first_name", "last_name"]
