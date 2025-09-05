from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from home.views import get_user_profile

class AuthRedirectMiddleware:
    """
    Bloqueio de rotas
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        public_urls = [reverse('login'), reverse('logout')]
        context = get_user_profile(request)
        is_authenticated = context.get("is_authenticated", False)
        
        if is_authenticated and request.path == reverse("login"):
            messages.error(request, "Caminho bloqueado.")
            return redirect("home")
        if not is_authenticated and request.path not in public_urls:
            messages.error(request, "Caminho bloquado, faça seu login.")
            return redirect("login")
        
        response = self.get_response(request)
        return response