from django.views import View
from . import decorators

class PreventWhenLoggedIn(View):
    def dispatch(self, request, *args, **kwargs):
        @decorators.prevent_when_logged_in
        def handler(req, *args, **kwargs):
            return View.dispatch(self, request, *args, **kwargs)
        return handler(request, *args, **kwargs)
