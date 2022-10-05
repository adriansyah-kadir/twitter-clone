from django import forms
from core_app import models

class TweetForm(forms.ModelForm):
    class Meta:
        model = models.Tweet
        fields = ['text', 'reply_mode', 'reply_to']
