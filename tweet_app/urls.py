from django.urls import path
from . import views


app_name = "tweet"
urlpatterns = [
    path("create/", views.Create.as_view(), name='create')
]
