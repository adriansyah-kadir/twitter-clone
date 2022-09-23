from django.urls import path
from . import views

app_name = "profile"
urlpatterns = [
    path("create/", views.Create.as_view(), name="create"),
    path("<id>/", views.Detail.as_view(), name="detail"),
]
