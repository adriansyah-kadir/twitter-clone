from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import os

# Create your models here.

def media_directory_path(instance, filename):
    return os.path.join("post", str(instance.tweet.id), filename)


User = get_user_model()

class Relation(models.Model):
    follower = models.ForeignKey(User, models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(User, models.CASCADE, related_name='following_set')

class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to="photo", null=True, blank=True)
    cover_photo = models.ImageField(upload_to="photo", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def following(self):
        return User.objects.filter(
            id__in=[relation.following.id for relation in Relation.objects.filter(follower=self.user)]
        )

    @property
    def followers(self):
        return User.objects.filter(
            id__in=[relation.follower.id for relation in Relation.objects.filter(following=self.user)]
        )


class Tweet(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, "posts_liked", blank=True)
    shares = models.ManyToManyField(User, "posts_shared", blank=True)
    mentions = models.ManyToManyField(User, 'tweet_mentions', blank=True)
    reply_mode = models.CharField(
        max_length=10,
        choices=(
            ('everyone', 'Everyone can reply'),
            ('following', 'People you follow'),
            ('mentioned', 'Only people you mention')
        ),
        default='everyone'
    )
    reply_to = models.ForeignKey("self", models.CASCADE, blank=True, null=True, related_name='replies')
    retweet = models.ForeignKey("self", models.CASCADE, blank=True, null=True, related_name='retweets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

    def liked_by(self, user):
        return self.likes.filter(id=user.id).first() != None

    def time_passed(self):
        delta = self.created_at - timezone.now()

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    text = models.TextField()

class Media(models.Model):
    tweet = models.ForeignKey(Tweet, models.CASCADE)
    file = models.FileField(upload_to=media_directory_path)
    content_type = models.CharField(max_length=20)
