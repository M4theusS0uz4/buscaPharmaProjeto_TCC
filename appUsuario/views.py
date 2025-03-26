import json
from urllib import request
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.template.defaultfilters import length
from django.core.mail import send_mail
from django.utils import timezone

from appAdminGeral.models import Evento
from appUsuario.models import Usuario
from appBusca.views2 import pegar_endereco_por_cep_e_numero,pegar_coordenadas_pelo_endereco

def verificar_existencia(request):
    email = request.GET.get('email', None)
    cpf = request.GET.get('cpf', None)

    resposta = {'email_existe': False, 'cpf_existe': False}

    if email and Usuario.objects.filter(email=email).exists():
        resposta['email_existe'] = True

    if cpf and Usuario.objects.filter(cpf=cpf).exists():
        resposta['cpf_existe'] = True

    return JsonResponse(resposta)

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['username']
        email = request.POST['email'].lower()
        cpf = request.POST['cpf']
        senha = request.POST['password']
        ddd = request.POST['ddd']
        telefone = ddd + request.POST['telefone']
        partes_nome = nome.split(' ')
        primeiro_nome = " ".join(partes_nome[0:len(partes_nome)-1])
        ultimo_nome = partes_nome[-1]
        if not Usuario.objects.filter(email=email).exists() and not Usuario.objects.filter(cpf=cpf).exists():
            user = Usuario(username=email, cpf=cpf, email=email, telefone=telefone,first_name=primeiro_nome, last_name=ultimo_nome)
            user.set_password(senha)
            user.save()
            send_mail(
                'Cadastrado com Sucesso',
                f'Bem vindo(a) ao BuscaPharma, {nome}!\n\nFaça já seus Agendamentos de Medicamentos.\n\nAtt.Equipe Busca.',
                'buscapharmatcc@gmail.com',  # Remetente
                [email],  # Destinatário
                fail_silently=False,
            )
            auth_login(request, user)
            return redirect('home')
    return render(request, 'cadastro.html')

def login(request):
    if request.user.is_authenticated:
        target = request.GET.get('next', None)
        return redirect(target or 'home')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        resposta = {'success': False, 'email_existe': False, 'senha': False, 'mensagem': ''}

        if email:
            usuarios = Usuario.objects.filter(email=email)

            if usuarios.exists():
                if usuarios.count() == 1:
                    usuario = usuarios.first()
                    if check_password(senha, usuario.password):
                        auth_login(request,usuario)
                        resposta['success'] = True
                        resposta['mensagem'] = 'Login bem-sucedido.'
                        return JsonResponse(resposta)  # Retorna JSON indicando sucesso
                    else:
                        resposta['senha'] = True
                        resposta['mensagem'] = 'Email ou senha incorretos.'
                else:
                    resposta['email_existe'] = True
                    resposta['mensagem'] = 'Múltiplos usuários encontrados com o mesmo email.'
            else:
                resposta['email_existe'] = True
                resposta['mensagem'] = 'Email não encontrado.'
        else:
            resposta['email_existe'] = True
            resposta['mensagem'] = 'O email é obrigatório.'

        return JsonResponse(resposta)
    return render(request, 'login.html')


# View de home
def home(request):
    data_atual = timezone.now()
    eventos = Evento.objects.filter(data_termino__gte=data_atual)
    for evento in eventos:
        endereco_evento = pegar_endereco_por_cep_e_numero(evento.id_unidade.cep, evento.id_unidade.numero)
        coordenadas = pegar_coordenadas_pelo_endereco(endereco_evento)
        evento.latitude = coordenadas[0]
        evento.longitude = coordenadas[1]

    return render(request, 'home.html', {'eventos': eventos})

def logout_usuario(request):
    logout(request)
    return redirect('home')