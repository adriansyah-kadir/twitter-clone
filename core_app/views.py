from django.shortcuts import render, reverse
from django.http import response, request
from django.contrib.auth import decorators
from . import models

# Create your views here.


@decorators.login_required
def index(req: request.HttpRequest):
    ctx = {}
    return render(req, "core/index.html", ctx)


@decorators.login_required
def search(req: request.HttpRequest):
    ctx = {}
    name = req.GET.get('name')
    if name:
        profiles = models.Profile.objects.filter(name__contains=name)
    else:
        profiles = models.Profile.objects.all()
    ctx['profiles'] = profiles
    return render(req, "core/search.html", ctx)
