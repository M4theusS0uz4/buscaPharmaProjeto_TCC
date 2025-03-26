import json
from urllib import request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.db.models import Count
from appAgendamento.models import Agendamento
from appBusca.models import Unidade
from appAdm.models import Admin


def cadastro_adm(request, id_unidade, username_admin):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST['password']
        nome_completo = request.POST.get('nome_completo')

        first_name = nome_completo.split()[0]
        last_name = nome_completo.split()[-1]

        # Verifica se todos os campos necessários estão preenchidos
        if nome_completo and senha and id_unidade and username:
            unidade = get_object_or_404(Unidade, pk=id_unidade)

            # Verifica se já existe um admin associado a essa unidade
            if Admin.objects.filter(username=username).exists():
                return render(request, 'cadastro_admin.html', {
                    'error': 'Já existe um administrador com esse username associado a esta unidade.',
                    'id_unidade': id_unidade,
                    'username_admin': username_admin
                })

            # Criando o usuário com a instância da Unidade
            user = Admin(username=username, id_unidade=unidade,email=email, is_staff=True, first_name=first_name,
                         last_name=last_name)
            user.set_password(senha)
            user.save()
            return redirect('home_admin_geral', username_admin)

    return render(request, 'cadastro_admin.html', {'id_unidade': id_unidade, 'username_admin': username_admin})



def login_adm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        token = request.POST.get('token')
        senha = request.POST.get('senha')

        if username and token and senha:
            try:
                admin = Admin.objects.get(username=username)
                # Verifica se o token (unidade) é válido
                if str(admin.id_unidade.pk) == token:  # Verifica se o token corresponde ao admin
                    if check_password(senha, admin.password):
                        auth_login(request, admin)
                        # Verifique se o usuário está logado após o auth_login
                        if request.user.is_authenticated:
                            return redirect('home_admin',id_admin =admin.id_admin)  # Redireciona para a home_admin diretamente
                        else:
                            return render(request, 'login_admin.html', {'mensagem': 'Falha ao autenticar o usuário.'})
                    else:
                        return render(request, 'login_admin.html', {'mensagem': 'Senha incorreta.'})
                else:
                    return render(request, 'login_admin.html', {'mensagem': 'Token não corresponde à unidade.'})

            except Admin.DoesNotExist:
                return render(request, 'login_admin.html', {'mensagem': 'Usuário não encontrado.'})

        return render(request, 'login_admin.html', {'mensagem': 'Todos os campos são obrigatórios.'})

    return render(request, 'login_admin.html')

def home_admin(request,id_admin):
        admin = Admin.objects.get(pk=id_admin)
        id_unidade = admin.id_unidade
        agendamentos = Agendamento.objects.filter(id_unidade=id_unidade,status='Agendado')
        return render(request, 'home_admin.html', {'agendamentos': agendamentos,'unidade':id_unidade,'id_admin':admin.id_admin})



def relatorio_produtos_interesse(request, id_unidade, id_admin):
    # Filtra os agendamentos pela unidade
    agendamentos = Agendamento.objects.filter(id_unidade=id_unidade)

    # Agrupa os agendamentos por produto e conta o total de interesses
    produtos_interesse = agendamentos.values('id_item__nome_item') \
        .annotate(total=Count('id_item')) \
        .order_by('-total')  # Ordena pelo total, do maior para o menor

    # Renderiza o template com os produtos e seus totais
    return render(request, 'relatorio_produtos_interesse.html', {'produtos_interesse': produtos_interesse, 'id_admin':id_admin,'id_unidade':id_unidade})

 # Importe seu modelo

def marcar_realizado(request, id_agendamento,id_admin):
    if request.method == 'POST':
        agendamento = get_object_or_404(Agendamento, id_agendamento=id_agendamento)
        # Atualize o status do agendamento para "realizado"
        agendamento.status = 'Realizado'  # Ou qualquer lógica que você tenha
        agendamento.save()
        return redirect('home_admin', id_admin=id_admin)  # Redireciona para a página de agendamentos

def relatorio_agendamentos_realizados(request,id_unidade,id_admin):
    # Filtro para agendamentos realizados (ajuste conforme sua lógica de status)
    agendamentos_realizados = Agendamento.objects.filter(status='Realizado', id_unidade=id_unidade)

    return render(request, 'relatorio_agendamentos_realizados.html', {'agendamentos': agendamentos_realizados, 'id_admin':id_admin,'id_unidade':id_unidade})



