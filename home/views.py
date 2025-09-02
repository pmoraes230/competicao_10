from django.shortcuts import render
from . import models

# Create your views here.
def list_user(request):
    context = {
        'users': models.Usuario.objects.all()
    }
    return render(request, "users/list_users.html", context)