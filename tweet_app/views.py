from django.shortcuts import render
from django.views import View
from django.contrib.auth import mixins
from django.http import request, response

# Create your views here.

class Create(mixins.LoginRequiredMixin, View):
    template_name = "tweet_app/create.html"
    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        return render(req, self.template_name, ctx)
