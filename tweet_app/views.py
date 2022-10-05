from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views import View
from django.contrib.auth import decorators
from django.http import request, response
from . import forms
from core_app import models, mixins
import json
import re

# Create your views here.

class Create(mixins.ProfileRequired, View):
    template_name = "tweet_app/create.html"
    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['form'] = forms.TweetForm()
        ctx['profiles'] = models.Profile.objects.all()
        return render(req, self.template_name, ctx)

    def post(self, req: request.HttpRequest, *args, **kwargs):
        mentions = json.loads(req.POST.get('mentions') or "[]")
        ctx = {}
        form = forms.TweetForm(req.POST)
        print(form.data)
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
        data = form.cleaned_data #text, reply_mode, mentions, reply_to
        if data.get('reply_to'):
            if data.get('reply_to').mentions.filter(id=req.user.id).first() == None and data.get('reply_to').user != req.user:
                return response.HttpResponse("not allowed to reply")
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
        tweet.mentions.add(*mentions)
        tweet.save()
        if image: image.save()
        if video: video.save()
        return redirect(reverse('index'))

class Detail(mixins.ProfileRequired, View):
    template_name = 'tweet_app/detail.html'
    def get(self, req: request.HttpRequest, *args, **kwargs):
        ctx = {}
        ctx['tweet'] = get_object_or_404(
            models.Tweet,
            id=kwargs.get('pk')
        )
        return render(req, self.template_name, ctx)

@decorators.login_required
def like(req: request.HttpRequest, *args, **kwargs):
    ctx = {}
    tweet = get_object_or_404(
        models.Tweet,
        pk=kwargs.get('pk')
    )
    if tweet.likes.filter(id=req.user.id):
        tweet.likes.remove(req.user)
        ctx['action'] = 'remove'
    else:
        tweet.likes.add(req.user)
        ctx['action'] = 'add'
    ctx['success'] = True
    return response.JsonResponse(ctx)
