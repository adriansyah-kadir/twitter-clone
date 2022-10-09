from django.shortcuts import render, reverse
from django.http import response, request
from . import models, decorators

# Create your views here.


@decorators.profile_required
def index(req: request.HttpRequest):
    ctx = {}
    tweets = models.Tweet.objects.filter(reply_to=None)
    ctx['tweets'] = tweets
    ctx['profile'] = req.user.profile
    return render(req, "core/index.html", ctx)


def search(req: request.HttpRequest):
    ctx = {}
    name = req.GET.get('name')
    if name:
        profiles = models.Profile.objects.filter(name__contains=name)
    else:
        profiles = models.Profile.objects.all()
    ctx['profiles'] = profiles
    return render(req, "core/search.html", ctx)

def notif(req: request.HttpRequest, *args, **kwargs):
    ctx = {}
    return render(req, "core/notif.html", ctx)
