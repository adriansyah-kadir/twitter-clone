from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import request
from core_app import models

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
