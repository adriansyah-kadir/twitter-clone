from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import os

# Create your models here.


def media_directory_path(instance, filename):
    return os.path.join("post", str(instance.tweet.id), filename)


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to="photo", null=True, blank=True)
    cover_photo = models.ImageField(upload_to="photo", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)
    date_of_birth = models.DateTimeField()


class Tweet(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, "post_likes")
    shares = models.ManyToManyField(User, "post_shares")
    mention = models.ManyToManyField(User, 'tweet_mentions', blank=True)
    reply_mode = models.CharField(
        max_length=10,
        choices=(
            ('everyone', 'Everyone can reply'),
            ('following', 'People you follow'),
            ('mentioned', 'Only people you mention')
        ),
        default='everyone'
    )


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    text = models.TextField()


class Reply(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    comment = models.ForeignKey(Comment, models.CASCADE)
    text = models.TextField()


class Media(models.Model):
    tweet = models.ForeignKey(Tweet, models.CASCADE)
    file = models.FileField(upload_to=media_directory_path)
    content_type = models.CharField(max_length=20)
