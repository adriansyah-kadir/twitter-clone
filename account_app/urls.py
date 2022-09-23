from django.urls import path
from . import views

app_name = "account"


urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("create/", views.Create.as_view(), name="create"),
    path("logout/", views.logout, name="logout"),
]
