from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def recaptcha_site_key():
    return settings.RECAPTCHA_SITE_KEY

@register.simple_tag
def tweet_liked_by(tweet, user):
    return tweet.liked_by(user)
