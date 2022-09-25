from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views import View
from django.contrib.auth import mixins
from django.http import request, response
from . import forms
from core_app import models
import json
import re

# Create your views here.

class Create(mixins.LoginRequiredMixin, View):
    template_name = "tweet_app/create.html"
    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.TweetForm()
        ctx['profiles'] = models.Profile.objects.all()
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        mentions = json.loads(req.POST.get('mentions'))
        ctx = {}
        form = forms.TweetForm(req.POST)
        image = req.FILES.get('image')
        video = req.FILES.get('video')
        ctx['form'] = form
        if image != None:
            if image.content_type not in ["image/png", "image/jpeg"]:
                ctx['error'] = "invalid content_type for image"
                print(ctx['error'])
                return render(req, self.template_name, ctx)
        if video != None:
            if video.content_type not in ["video/mp4", "video/3gp"]:
                ctx['error'] = "invalid content_type for video"
                print(ctx['error'])
                return render(req, self.template_name, ctx)
        if not form.is_valid():
            ctx['error'] = "invalid input"
            return render(req, self.template_name, ctx)
        data = form.cleaned_data #text, reply_mode, mentions
        if re.match('^\s+$', data['text']) or len(data['text']) <= 0:
            if not (image or video):
                ctx['error'] = "provide at least one of text, video or image"
                return render(req, self.template_name, ctx)
        tweet = models.Tweet.objects.create(
            user=req.user,
            **data
        )
        if image != None:
            image = models.Media.objects.create(
                tweet=tweet,
                file=image,
                content_type=image.content_type
            )
        if video != None:
            video = models.Media.objects.create(
                tweet=tweet,
                file=video,
                content_type=video.content_type
            )
        tweet.mention.add(*mentions)
        tweet.save()
        if image: image.save()
        if video: video.save()
        return redirect(reverse('index'))
