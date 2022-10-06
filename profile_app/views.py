from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http import request, response
from core_app import mixins, models
from django.core import serializers
from . import forms
import re

# Create your views here.


class Detail(View):
    template_name = "profile_app/detail.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        profile = get_object_or_404(models.Profile, id=kwargs.get("id"))
        ctx["profile"] = profile
        return render(req, self.template_name, ctx)

class Update(mixins.ProfileRequired, View):
    template_name = "profile_app/update.html"
    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['profile'] = req.user.profile
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        print(req.POST, req.FILES)

class Create(View):
    template_name = "profile_app/update.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.ProfileForm()
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.ProfileForm(req.POST, req.FILES)
        if ctx['form'].is_valid():
            data = ctx['form'].cleaned_data
            profile = models.Profile.objects.create(
                user=req.user,
                **data
            )
            profile.save()
            if req.GET.get('next'):
                return redirect(req.GET.get('next'))
            return redirect('/')
        else:
            return render(req, self.template_name, ctx)

def profile_all(req: request.HttpRequest, *args, **kwargs):
    users = models.User.objects.filter(
        username__contains=req.GET.get('name')
    )
    profiles = [user.profile for user in users]
    data = {
            'profiles':[
        {
            'id': profile.user.id,
            'photo': False if profile.photo.name == '' else profile.photo.url,
            'name': profile.name,
            'user': {
                'username': profile.user.username
            }
        } for profile in profiles
    ]
    }
    return response.JsonResponse(data)
