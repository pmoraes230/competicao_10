from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_user, name="list_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/<int:id_user>/", views.update_user, name="update_user"),
    path("delete_user/<int:id_user>/", views.delete_user, name="delete_user")
]
