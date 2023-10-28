from django.urls import path
from pmiot import views

urlpatterns = [
    path("", views.home, name="home"),
]
