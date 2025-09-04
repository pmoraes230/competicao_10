from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from . import models
import uuid
import pdfkit

# Create your views here
def get_user_profile(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = models.Usuario.objects.select_related("perfil").get(id_usuario=user_id)
            return {
                'user_id': user.id_usuario,
                'user_name': user.nome_usuario,
                'user_role': user.perfil.nome_perfil,
                'is_authenticated': True
            }
        except models.Usuario.DoesNotExist:
            return {"user_name": "", "is_authenticated": False}
    return {"user_name": "", "is_authenticated": False}

def login(request):
    if request.method == "GET":
        return render(request, "login/login.html")
    
    if request.method == "POST":
        login = request.POST.get("login")
        senha = request.POST.get("senha")
        
        if not all([login, senha]):
            messages.info(request, "Informe suas crendenciais antes de fazer o login")
            return redirect("login")
        
        if models.Usuario.objects.filter(email_usuario=login).first() or models.Usuario.objects.filter(cpf_usuario=login).first():
            user = models.Usuario.objects.filter(email_usuario=login).first() or models.Usuario.objects.filter(cpf_usuario=login).first()
            if check_password(senha, user.senha_usuario):
                request.session['user_id'] = user.id_usuario
                request.session['user_name'] = user.nome_usuario
                request.session['user_role'] = user.perfil.nome_perfil
                
                if user.perfil.nome_perfil == "Validador":
                    return redirect("validador")
                return redirect("home")
            else:
                messages.error(request, "Senha incorreta.")
                return redirect("login")
        else:
            messages.error(request, "Usuário não encontrado.")
            return redirect("login")
        
def logoutView(request):
    logout(request)
    messages.success(request, "Você saiu do sistema")
    return redirect("login")

def home(request):
    context = {
        'events': models.Evento.objects.all(),
        **get_user_profile(request)
    }
    return render(request, "home/home.html", context)

def list_user(request):
    context = {
        'users': models.Usuario.objects.all(),
        **get_user_profile(request)
    }
    return render(request, "users/list_users.html", context)

def register_user(request):
    context = {
        'perfis': models.Perfil.objects.all(),
        **get_user_profile(request)
    }
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        perfil_id = request.POST.get("perfil_id")
        senha1 = request.POST.get("senha1")
        senha2 = request.POST.get("senha2")
        
        if not all([nome, cpf, email, perfil_id, senha1, senha2]):
            messages.info(request, "Não pode fazer o cadastro com campos em branco")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(cpf_usuario=cpf).exists():
            messages.info(request, "CPF já cadastrado")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(email_usuario=email).exists():
            messages.info(request, "Email já cadastrado")
            return redirect("register_user")
        
        if senha1 != senha2:
            messages.info(request, "Senhas não são iguais")
            return redirect("register_user")
        
        try:
            perfil = models.Perfil.objects.get(id_perfil=perfil_id)
        except models.Perfil.DoesNotExist:
            messages.error(request, "Perfil não encontrado")
            return redirect("register_user")
        
        senha_cript = make_password(senha1)
        
        try:
            novo_usuario = models.Usuario.objects.create(
                nome_usuario=nome,
                email_usuario=email,
                cpf_usuario=cpf,
                senha_usuario=senha_cript,
                perfil=perfil
            )
            novo_usuario.full_clean()
            novo_usuario.save()
            
            messages.success(request, f"Usuário {novo_usuario.nome_usuario} cadastrado com sucesso!.")
            return redirect("list_user")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar usuário {ve}")
            return redirect("register_user")
        
    return render(request, "users/register_user.html", context)

def update_user(request, id_user):
    user = models.Usuario.objects.get(id_usuario=id_user)
    context = {
        'perfis': models.Perfil.objects.all(),
        'user': user,
        **get_user_profile(request)
    }
    
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        perfil_id = request.POST.get("perfil_id")
        
        if not all([nome, cpf, email, perfil_id]):
            messages.info(request, "Não pode fazer o cadastro com campos em branco")
            return redirect("update_user", id_user=id_user)
        
        if models.Usuario.objects.filter(cpf_usuario=cpf).exclude(id_usuario=id_user).exists():
            messages.info(request, "CPF já cadastrado")
            return redirect("update_user", id_user=id_user)
        
        if models.Usuario.objects.filter(email_usuario=email).exclude(id_usuario=id_user).exists():
            messages.info(request, "Email já cadastrado")
            return redirect("update_user", id_user=id_user)
        
        try:
            perfil = models.Perfil.objects.get(id_perfil=perfil_id)
        except models.Perfil.DoesNotExist:
            messages.error(request, "Perfil não encontrado")
            return redirect("update_user", id_user=id_user)
        
        try:
            user.nome_usuario = nome
            user.cpf_usuario = cpf
            user.email_usuario = email
            user.perfil = perfil
            
            user.full_clean()
            user.save()
            
            messages.success(request, f"Cadastro do usuário {user.nome_usuario} atualizado com sucesso!.")
            return redirect("list_user")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar usuário {ve}")
            return redirect("update_user", id_user=id_user)
         
    return render(request, "users/update_user.html", context)

def delete_user(request, id_user):
    try:
        user = models.Usuario.objects.get(id_usuario=id_user)
        if request.method == "POST":
            user.delete()
            messages.success(request, "Usuário apagado do sistema.")
            return redirect("list_user")
        context = {
            "user": user,
            **get_user_profile(request)
        }
        return render(request, "users/delete_user.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("list_user")
    
def deteils_event(request, id_event):
    event = models.Evento.objects.get(id_evento=id_event)
    setores = models.Setor.objects.filter(evento_id_evento=event)
    search_client = None
    client = None
    
    if request.method == "POST" and "search" in request.POST:
        input_client = request.POST.get("search_client")
        if input_client:
            search_client = models.Cliente.objects.filter(
                Q(nome_cliente__icontains=input_client)
            )
            if not search_client:
                messages.error(request, "Cliente pesquisado não encontrado no sistema.")
            else:
                messages.success(request, f"{search_client.count()} cliente com esse nome encontrado")
        else:
            messages.info(request, "Insira um nome de um cliente antes de pesquisar.")
    
    if request.method == "POST" and "select_client" in request.POST:
        input_client_select = request.POST.get("id_client")
        request.session["client"] = input_client_select
        if input_client_select:
            client = models.Cliente.objects.get(id_cliente=input_client_select)
            messages.success(request, f"Cliente {client.nome_cliente} selecionado.")
        else:
            messages.info(request, "Selecione um cliente")
     
    context = {
        "event": event,
        "search_client": search_client,
        "client": client,
        "setores": setores,
        **get_user_profile(request)
    }
    return render(request, "events/deteils_event.html", context)

def buy_ticket(request, id_event):
    event = models.Evento.objects.get(id_evento=id_event)
    setores = models.Setor.objects.filter(evento_id_evento=event)
    search_client = None
    
    if request.method == "POST" and "buy_ticket" in request.POST:
        client_id = request.session.get("client")
        try:
            client = models.Cliente.objects.get(id_cliente=client_id)
        except models.Cliente.DoesNotExist:
            messages.error(request, "Cliente não encontrado")
            return redirect("deteils_event", id_event=id_event)
        
        setor_id = request.POST.get("evento_id")
        qtd_ingressos = int(request.POST.get("qtd_ingressos"), 0)
        
        if not all([setor_id, qtd_ingressos]):
            messages.info(request, "Selecione o setor e a quantidade de ingressos")
        
        try:
            setor = models.Setor.objects.get(id_setor=setor_id)
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("deteils_event", id_event=id_event)
        
        if qtd_ingressos > setor.limite_setor:
            messages.info(request, "A quantiade de ingresso excedeu o limite de ingressos disponíveis no setor")
        elif qtd_ingressos <= 0:
            messages.info(request, "Selecione um ingresso antes de comprar")
        else:
            tickets = []
            for _ in range(qtd_ingressos):
                ticket =  models.Ingresso.objects.create(
                    cliente=client,
                    evento=event,
                    setor=setor,
                    id_ingresso=str(uuid.uuid4()),
                    data_emissao_ingresso=timezone.now(),
                    status_ingresso='emitido'
                )
                setor.limite_setor -= 1
                setor.save()
                
                ticket.full_clean()
                ticket.save()
            tickets.append(ticket)
                
            messages.success(request, "Ingresso emitido(s)")
            return redirect("deteils_event", id_event=id_event)
            
    context = {
        "event": event,
        "search_client": search_client,
        "client": client,
        "setores": setores,
        **get_user_profile(request)
    }
    return render(request, "events/deteils_event.html", context)

def ticket_generate(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id_evento=id_event)
    context.update({
        'event': models.Evento.objects.get(id_evento=id_event),
        'tickets': models.Ingresso.objects.filter(evento=event)  
    })
    return render(request, "events/tickets_generate.html", context)

def register_event(request):
    context = get_user_profile(request)
    if request.method == "POST":
        nome_evento = request.POST.get("nome")
        limite_pessoas = request.POST.get("limite_pessoas")
        data_evento = request.POST.get("data_evento")
        horario_evento = request.POST.get("horario_evento")
        imagem_evento = request.FILES.get("imagem_evento")
        descricao_evento = request.POST.get("descricao_evento")
        
        if not all([nome_evento, limite_pessoas, data_evento, horario_evento, imagem_evento, descricao_evento]):
            messages.info(request, "Não pode fazer o cadastro com campos em branco")
            return redirect("register_event")
        
        if models.Evento.objects.filter(data_evento=data_evento, horario_evento=horario_evento):
            messages.error(request, "Evento já com essa data e horario")
            return redirect("register_event")
        
        user_id = 1
        try:
            user = models.Usuario.objects.get(id_usuario=user_id)
        except models.Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return redirect("register_event")
        
        try:
            novo_evento = models.Evento.objects.create(
                nome_evento=nome_evento,
                limitepessoas_evento=limite_pessoas,
                data_evento=data_evento,
                horario_evento=horario_evento,
                descricao_evento=descricao_evento,
                imagem_evento=imagem_evento,
                usuario_id_usuario=user
            )
            novo_evento.full_clean()
            novo_evento.save()
            
            messages.success(request, f"Evento {novo_evento.nome_evento} criado com sucesso!.")
            return redirect("deteils_event", id_event=novo_evento.id_evento)
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar o usuário {str(ve)}")
            return redirect("register_event")
        
    return render(request, "events/register_event.html", context)

def update_event(request, id_event):
    evento = models.Evento.objects.get(id_evento=id_event)
    
    if request.method == "POST":
        nome_evento = request.POST.get("nome")
        limite_pessoas = request.POST.get("limite_pessoas")
        data_evento = request.POST.get("data_evento")
        horario_evento = request.POST.get("horario_evento")
        imagem_evento = request.FILES.get("imagem_evento")
        descricao_evento = request.POST.get("descricao_evento")
        
        if not all([nome_evento, limite_pessoas, data_evento, horario_evento, descricao_evento]):
            messages.info(request, "Não pode fazer o cadastro com campos em branco")
            return redirect("update_event", id_event=id_event)
        
        if models.Evento.objects.filter(data_evento=data_evento, horario_evento=horario_evento).exclude(id_evento=id_event):
            messages.error(request, "Evento já com essa data e horario")
            return redirect("update_event", id_event=id_event)
        
        user_id = 1
        try:
            user = models.Usuario.objects.get(id_usuario=user_id)
        except models.Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return redirect("update_event", id_event=id_event)
        
        try:
            evento.nome_evento=nome_evento
            evento.limitepessoas_evento=limite_pessoas
            evento.data_evento=data_evento
            evento.horario_evento=horario_evento
            evento.descricao_evento=descricao_evento
            if imagem_evento:
                evento.imagem_evento=imagem_evento
            evento.usuario_id_usuario=user
                
            evento.full_clean()
            evento.save()
            
            messages.success(request, f"Cadastro do evento {evento.nome_evento} atualizado com sucesso!.")
            return redirect("update_event", id_event=id_event)
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar o usuário {str(ve)}")
            return redirect("update_event", id_event=id_event)
    
    context = {
        'evento': evento,
        **get_user_profile(request)
    }
    return render(request, "events/update_event.html", context)

def delete_event(request, id_event):
    try:
        evento = models.Evento.objects.get(id_evento=id_event)
        if request.method == "POST":
            evento.delete()
            messages.success(request, "Evento apagado do sistema.")
            return redirect("home")
        context = {
            "evento": evento,
            **get_user_profile(request)
        }
        return render(request, "events/delete_event.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("home")
    
def list_setores(request, id_event):
    setores = models.Setor.objects.filter(evento_id_evento=id_event)
    evento = models.Evento.objects.get(id_evento=id_event)
    context = {
        'setores': setores,
        'evento': evento,
        **get_user_profile(request)
    }
    return render(request, "setores/lista_setores.html", context)

def delete_setor(request, id_setor):
    try:
        setor = models.Setor.objects.get(id_setor=id_setor)
        if request.method == "POST":
            setor.delete()
            messages.success(request, "Setor apagado do sistema.")
            return redirect("home")
        context = {
            "setor": setor,
            **get_user_profile(request)
        }
        return render(request, "setores/delete_setor.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("deteils_event", id_event=setor.evento_id_evento.id_evento)
    
def register_setor(request, id_event):
    evento_session = models.Evento.objects.get(id_evento=id_event)
    context = {
        'eventos': models.Evento.objects.all(),
        'evento_session': evento_session,
        **get_user_profile(request)
    }
    if request.method == "POST":
        nome = request.POST.get("nome")
        qtd_ingresso = request.POST.get("qtd_ingresso")
        preco_setor = request.POST.get("preco_setor")
        evento_id = request.POST.get("evento_id")
        
        if not all([nome, qtd_ingresso, preco_setor, evento_id]):
            messages.info(request, "Não pode fazer o cadastro com campos em branco")
            return redirect("register_setor", id_event=evento_session.id_evento)
        
        try:
            evento = models.Evento.objects.get(id_evento=evento_id)
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("register_setor", id_event=evento_session.id_evento)
        
        try:
            novo_setor = models.Setor.objects.create(
                nome_setor=nome,
                limite_setor=qtd_ingresso,
                preco_setor=preco_setor,
                evento_id_evento=evento
            )
            novo_setor.full_clean()
            novo_setor.save()
            
            messages.success(request, f"Setor {novo_setor.nome_setor} criado com sucesso.")
            return redirect("lista_setores", id_event=evento_session.id_evento)
        
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo setor: {str(ve)}")
        
    return render(request, "setores/register_setor.html", context)

def update_setor(request, id_setor):
    setor = models.Setor.objects.get(id_setor=id_setor)
    context = {
        "setor": setor,
        'eventos': models.Evento.objects.all(),
        **get_user_profile(request)
    }
    if request.method == "POST":
        nome = request.POST.get("nome")
        qtd_ingresso = request.POST.get("qtd_ingresso")
        preco_setor = request.POST.get("preco_setor")
        evento_id = request.POST.get("evento_id")
        
        if not all([nome, qtd_ingresso, preco_setor, evento_id]):
            messages.info(request, "Não pode fazer o cadastro com campos em branco")
            return redirect("update_setor", id_setor=id_setor)
        
        try:
            evento = models.Evento.objects.get(id_evento=evento_id)
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("update_setor", id_setor=id_setor)
        
        try:
            setor.nome_setor = nome
            setor.limite_setor = qtd_ingresso
            setor.preco_setor = preco_setor
            setor.evento_id_evento = evento
            
            setor.full_clean()
            setor.save()
            
            messages.success(request, f"Setor {setor.nome_setor} criado com sucesso.")
            return redirect("lista_setores", id_event=setor.evento_id_evento.id_evento)
        
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo setor: {str(ve)}")
    return render(request, "setores/update_setores.html", context)
    
def register_client(request, id_event):
    context = get_user_profile(request)
    context['event'] = models.Evento.objects.get(id_evento=id_event)
    
    if request.method == "POST":
        nome_cliente = request.POST.get("nome_cliente")
        email_cliente = request.POST.get("email_cliente")
        cpf_cliente = request.POST.get("cpf")
        
        if not all([nome_cliente, email_cliente, cpf_cliente]):
            messages.info(request, "Preencha todos os campos antes de cadastrar")
            return redirect("register_client", id_event=id_event)
        
        if models.Cliente.objects.filter(cpf_cliente=cpf_cliente).exists():
            messages.info(request, "CPF já cadastrado no sistema.")
            return redirect("register_client", id_event=id_event)
        
        if models.Cliente.objects.filter(email_cliente=email_cliente).exists():
            messages.info(request, "Email já cadastrado no sistema.")
            return redirect("register_client", id_event=id_event)
        
        try:
            novo_cliente = models.Cliente.objects.create(
                nome_cliente=nome_cliente,
                cpf_cliente=cpf_cliente,
                email_cliente=email_cliente
            )
            novo_cliente.full_clean()
            novo_cliente.save()
            
            messages.success(request, f"Cliente {novo_cliente.nome_cliente} cadastrado com sucesso no sistema!.")
            return redirect("deteils_event", id_event=id_event)
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar cliente no sistema: {str(ve)}")
        
    return render(request, "events/register_client.html", context)

def export_ticket(request, id_ticket):
    ticket = get_object_or_404(models.Ingresso, id_ingresso=id_ticket)
    html = render_to_string("events/ticket.html", {'ticket': ticket})
    configuration = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    
    options = {
        'page-size': 'A6',
        # 'page-width': '80mm',
        # 'page-height': '160mm',
        'encoding': "UTF-8",
    }
    
    pdf = pdfkit.from_string(html, False, configuration=configuration, options=options)
    try:
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="Ingresso_evento_{ticket.evento.nome_evento}_cliente_{ticket.cliente.nome_cliente}.pdf"'
        response.write(pdf)
        
        return response
    except ValueError as ve:
        return HttpResponse(f"Erro ao gerar pdf: {str(ve)}")