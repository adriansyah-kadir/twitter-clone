from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name='search'),
    path("profile/", include("profile_app.urls")),
    path("account/", include("account_app.urls")),
    path("tweet/", include("tweet_app.urls")),
    # path('post/', include('post_app.urls')),
    # path('comment/', include('comment_app.urls')),
]
