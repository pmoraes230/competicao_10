from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models

# Create your views here.
def validador(request):
    context = get_user_profile(request)
    
    if request.method == "POST":
        id_input = request.POST.get("id_ticket").strip()
        try:
            ticket = models.Ingresso.objects.get(id_ingresso=id_input)
            if ticket.status_ingresso == "validado":
                messages.info(request, "Ingresso já validado no sistema. Valide outro ingresso.")
                return redirect("validador")
            elif ticket.status_ingresso == "cancelado":
                messages.info(request, "Ingresso cancelado. Valide outro ingresso.")
                return redirect("validador")
            elif ticket.status_ingresso == "emitido":
                ticket.status_ingresso = "validado"
                ticket.save()
                messages.success(request, "Ingresso validado com sucesso. Bom Evento!.")
                return redirect("validador")
        except models.Ingresso.DoesNotExist:
            messages.error(request, "Ingresso não encontrado no sistema.")
            return redirect("validador")
    
    return render(request, "validador.html", context)