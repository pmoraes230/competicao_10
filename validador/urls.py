from django.urls import path
from . import views

urlpatterns = [
    path("validador/", views.validador, name="validador")
]
