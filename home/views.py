from django.shortcuts import render

# Create your views here.
def list_user(request):
    return render(request, "users/list_user.html")