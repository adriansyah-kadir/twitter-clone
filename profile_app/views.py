from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import request, response
from core_app import models
from django.core import serializers

# Create your views here.


class Detail(View):
    template_name = "profile_app/detail.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        profile = get_object_or_404(models.Profile, id=kwargs.get("id"))
        ctx["profile"] = profile
        return render(req, self.template_name, ctx)


class Create(View):
    template_name = "profile_app/create.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        pass

def profile_all(req: request.HttpRequest, *args, **kwargs):
    profiles = models.Profile.objects.filter(
        name__contains=req.GET.get('name')
    )
    data = {
            'profiles':[
        {
            'id': profile.id,
            'photo': profile.photo.url,
            'name': profile.name,
            'user': {
                'username': profile.user.username
            }
        } for profile in profiles
    ]
    }
    return response.JsonResponse(data)
