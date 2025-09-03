from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from . import models

# Create your views here.
def list_user(request):
    context = {
        'users': models.Usuario.objects.all()
    }
    return render(request, "users/list_users.html", context)

def register_user(request):
    context = {
        'perfis': models.Perfil.objects.all()
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
        'user': user
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
            "user": user
        }
        return render(request, "users/delete_user.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("list_user")