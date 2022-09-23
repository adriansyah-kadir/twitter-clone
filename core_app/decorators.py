from django.http import request, response
from django.shortcuts import redirect

def prevent_when_logged_in(func, redirect_to=None):
    def decorator(req: request.HttpRequest, *args, **kwargs):
        if req.user.is_authenticated:
            if redirect_to:
                return redirect(redirect_to)
            raise response.Http404
        return func(req, *args, **kwargs)
    return decorator
