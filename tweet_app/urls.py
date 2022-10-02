from django.urls import path
from . import views


app_name = "tweet"
urlpatterns = [
    path("create/", views.Create.as_view(), name='create'),
    path('likes/<pk>/', views.like, name='like'),
    path('<pk>/', views.Detail.as_view(), name='detail'),
]
