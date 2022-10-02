from django.http import request, response
from django.shortcuts import redirect
from django.contrib.auth import decorators
from django.conf import settings

def prevent_when_logged_in(func=None, redirect_to=None):
    def decorator(req: request.HttpRequest, *args, **kwargs):
        if req.user.is_authenticated:
            if redirect_to:
                return redirect(redirect_to)
            raise response.Http404
        return func(req, *args, **kwargs)
    if func:
        return decorator
    def d(f):
        def decorator(req: request.HttpRequest, *args, **kwargs):
            if req.user.is_authenticated:
                if redirect_to:
                    return redirect(redirect_to)
                raise response.Http404
            return f(req, *args, **kwargs)
        return decorator
    return d

def profile_required(func=None, redirect_to=None):
    def decorator(req: request.HttpRequest, *args, **kwargs):
        if hasattr(req.user, 'profile'):
            return func(req, *args, **kwargs)
        if redirect_to:
            return redirect(redirect_to)
        return redirect(settings.PROFILE_URL)
    return decorators.login_required(decorator)
    if func:
        return decorator
    def d(f):
        def decorator(req: request.HttpRequest, *args, **kwargs):
            if req.user.is_authenticated:
                if redirect_to:
                    return redirect(redirect_to)
                raise response.Http404
            return f(req, *args, **kwargs)
        return decorator
    return d
