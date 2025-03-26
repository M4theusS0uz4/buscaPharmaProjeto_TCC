import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls.base import reverse

from appUsuario.models import Usuario
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Variável para armazenar os códigos temporariamente
codes = {}


def redefinir_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Usuario.objects.filter(email=email).first()
        if user:
            # Gerar código aleatório
            codigo_verificacao = random.randint(100000, 999999)

            # Armazenar código na variável 'codes' para validar depois
            codes[email] = codigo_verificacao
            # Enviar código por e-mail
            send_mail(
                'Código de Verificação',
                f'Seu código de verificação é: {codigo_verificacao}',
                'buscapharmatcc@gmail.com',  # Remetente
                [email],  # Destinatário
                fail_silently=False,
            )

            # Redirecionar para a página de verificação de código
            return redirect(reverse('verificar_codigo', kwargs={'email': email}))
        else:
            messages.error(request, 'Email não encontrado.')

    return render(request, 'redefinir_senha.html')


def verificar_codigo(request, email):
    if request.method == 'POST':
        codigo_inserido = request.POST.get('codigo')

        # Verificar se o código inserido corresponde ao código enviado
        if codes.get(email) == int(codigo_inserido):
            # Código correto, redirecionar para redefinir senha
            return redirect(reverse('nova_senha', kwargs={'email':email}))
        else:
            messages.error(request, 'Código inválido. Tente novamente')

    return render(request, 'verificar_codigo.html',{'email': email})





def nova_senha(request, email):
    user = Usuario.objects.get(email=email)

    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')

        # Verifica se o campo de nova senha não está vazio
        if not nova_senha:
            messages.error(request, 'O campo nova senha não pode ser vazio.')
            return render(request, 'nova_senha.html', {'email': email})

        # Verifica se a nova senha é igual à senha atual
        if user.check_password(nova_senha):
            messages.error(request, 'A nova senha não pode ser a mesma que a senha antiga.')
            return render(request, 'nova_senha.html', {'email': email})

        # Atualizar a senha
        user.password = make_password(nova_senha)
        user.save()

        return redirect('login')

    return render(request, 'nova_senha.html', {'email': email})
