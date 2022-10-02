from django.views import View
from . import decorators

class PreventWhenLoggedIn(View):
    redirect_to = '/'
    def dispatch(self, request, *args, **kwargs):
        @decorators.prevent_when_logged_in(redirect_to=self.redirect_to)
        def handler(req, *args, **kwargs):
            return View.dispatch(self, request, *args, **kwargs)
        return handler(request, *args, **kwargs)

class ProfileRequired(View):
    def dispatch(self, request, *args, **kwargs):
        @decorators.profile_required
        def handler(req, *args, **kwargs):
            return View.dispatch(self, request, *args, **kwargs)
        return handler(request, *args, **kwargs)
