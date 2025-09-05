from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, base64, io

# Create your views here.
def dashboard(request):
    context = get_user_profile(request)
    event, grafic_setors = None, []
    
    if request.method == "POST":
        id_event = request.POST.get("id_event")
        if not id_event:
            messages.error(request, "Selecione um evento antes de pesquisar")
            return redirect("dashboard")
        try:
            event = models.Evento.objects.get(id_evento=id_event)
            
            for setor in models.Setor.objects.filter(evento_id_evento=event):
                counts = {
                    'Limite ingressos': setor.limite_setor,
                    'Emitidos': models.Ingresso.objects.filter(evento=event, setor=setor, status_ingresso='emitido').count(),
                    'Validados': models.Ingresso.objects.filter(evento=event, setor=setor, status_ingresso='validado').count(),
                    'Cancelado': models.Ingresso.objects.filter(evento=event, setor=setor, status_ingresso='cancelado').count(),
                }
                
                ingressos_total = counts['Emitidos'] + counts["Validados"]
                limite_setor = counts["Limite ingressos"]
                ocupacao_percentual = (ingressos_total / (limite_setor+ingressos_total) * 100) if limite_setor > 0 else 0
                
                alerta = None
                if ocupacao_percentual >= 90 and ocupacao_percentual < 100:
                    alerta = f"O setor {setor.nome_setor} está quase lotado ({ocupacao_percentual:.1f}% da capacidade)!"
                elif ocupacao_percentual >= 100:
                    alerta = f"O setor {setor.nome_setor} está lotado!"
                
                data = [v for v in counts.values() if v>0]
                labels = [f"{k}" for k,v in counts.items() if v>0] 
                if not data: continue
                
                fig, ax = plt.subplots()
                bars = ax.bar(np.arange(len(data)), data, color=["#1331A1", "#F8B62F", "#A2CA02", "#0C0C0C"][:len(data)])
                ax.set_title(f"Setor: {setor.nome_setor}")
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(labels, rotation=0, ha="center")
                for bar in bars:
                    ax.text(bar.get_x(), bar.get_width()/2 + bar.get_height(), str(int(bar.get_height())),
                            ha="center", va="bottom")
                    
                buf = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf, format="png")
                plt.close(fig)
                
                grafic_setors.append({
                    "setor": setor.nome_setor, 
                    "grafic": base64.b64encode(buf.getvalue()).decode,
                    "alerta": alerta
                })
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado no sistema")
            return redirect("dashboard")
    
    context.update({
        'events': models.Evento.objects.all(),
        'event': event,
        'grafic_setors': grafic_setors
    })
    return render(request, "dashboard.html", context)
