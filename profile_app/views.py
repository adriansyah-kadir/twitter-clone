from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views import View
from django.http import request, response
from core_app import mixins, models, decorators
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
        ctx["following"] = profile.followers.filter(id=req.user.id).first() != None
        return render(req, self.template_name, ctx)

class Update(mixins.ProfileRequired, View):
    template_name = "profile_app/update.html"
    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['profile'] = req.user.profile
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.UpdateProfileForm(req.POST, req.FILES)
        ctx['profile'] = req.user.profile
        if ctx['form'].is_valid():
            data = {}
            data2 = ctx['form'].cleaned_data
            for k in data2:
                if data2[k]:
                    data[k] = data2[k]
            for k in data:
                ctx['profile'].__dict__[k] = data[k]
            ctx['profile'].save()
            return redirect(reverse('profile:detail', kwargs={'id': ctx['profile'].id}))

        return render(req, self.template_name, ctx)

class Create(View):
    template_name = "profile_app/create.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.ProfileForm()
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.ProfileForm(req.POST, req.FILES)
        if ctx['form'].is_valid():
            print("valid")
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

def unfollow(req: request.HttpRequest, *args, **kwargs):
    if req.method != "POST":
        return response.HttpResponseNotAllowed(['POST'])
    user = get_object_or_404(models.User, id=req.POST.get('user'))
    if user == req.user: return response.HttpResponse("cant unfollow self")
    req.user.profile.unfollow(user)
    return redirect(reverse('profile:detail', kwargs={'id': user.profile.id}))

def follow(req: request.HttpRequest, *args, **kwargs):
    if req.method != "POST":
        return response.HttpResponseNotAllowed(['POST'])
    user = get_object_or_404(models.User, id=req.POST.get('user'))
    if user == req.user: return response.HttpResponse("cant follow self")
    req.user.profile.follow(user)
    return redirect(reverse('profile:detail', kwargs={'id': user.profile.id}))
