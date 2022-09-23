from django.shortcuts import redirect, render, reverse
from django.views import View
from django.http import request
from . import forms
from core_app import decorators, models, mixins
from django.contrib.auth import authenticate, login, logout as auth_logout
from core_app import utils

# Create your views here.

class Login(mixins.PreventWhenLoggedIn, View):
    template_name = "account_app/login.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {
            'input': {}
        }
        username = req.POST.get("username")
        password = req.POST.get("password")
        next_url = req.GET.get("next")
        token = req.POST.get('g-recaptcha-response')
        ctx['input']["username"] = username
        ctx["input"]["password"] = password

        if not utils.verify_recaptcha(token):
            ctx["captcha"] = "failed to validate recaptcha"
            return render(req, self.template_name, ctx)

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(req, user)
                return redirect(next_url or reverse("index"))

        return render(req, self.template_name, ctx)


class Create(View):
    template_name = "account_app/create.html"

    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        form = forms.UserForm()
        ctx["form"] = form
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        form = forms.UserForm(req.POST)
        token = req.POST.get('g-recaptcha-response')

        if not utils.verify_recaptcha(token):
            ctx['error'] = 'cannot verify recaptcha'
            return render(req, self.template_name, ctx)

        if form.is_valid():
            data = form.cleaned_data
            user = models.User.objects.create_user(**data)
            return redirect(reverse("account:login") + f"?{req.GET.urlencode()}")

        ctx["form"] = form

        return render(req, self.template_name, ctx)


def logout(req: request.HttpRequest, *args, **kwargs):
    param = req.GET.urlencode()
    auth_logout(req)
    return redirect(reverse("account:login") + f"?{param}")
