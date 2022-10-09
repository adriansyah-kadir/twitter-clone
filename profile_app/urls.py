from django.urls import path
from . import views

app_name = "profile"
urlpatterns = [
    path("create/", views.Create.as_view(), name="create"),
    path("search/", views.profile_all, name='search'),
    path("update/", views.Update.as_view(), name='update'),
    path("unfollow/", views.unfollow, name='unfollow'),
    path("follow/", views.follow, name='follow'),
    path("<id>/", views.Detail.as_view(), name="detail"),
]
