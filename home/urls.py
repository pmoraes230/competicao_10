from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_user, name="list_user")
]
