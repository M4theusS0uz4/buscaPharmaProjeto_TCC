from django.contrib.messages.context_processors import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from appAdm.models import Admin
from appUsuario.models import Usuario


def editar_perfil_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('username')  # Corrigido para 'username'
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        ddd = request.POST.get('ddd')
        telefone = ddd + request.POST.get('telefone')
        # Verifica se todos os campos estão preenchidos
        if all([nome, email, cpf, ddd, telefone]):
            try:
                usuario = get_object_or_404(Usuario, cpf=cpf)  # Usa get_object_or_404 para lidar com o caso em que o usuário não é encontrado
                partes_nome = nome.split(' ')
                primeiro_nome = " ".join(partes_nome[:-1])  # Nome sem o último sobrenome
                ultimo_nome = partes_nome[-1]  # Último sobrenome

                # Atualiza os dados do usuário
                usuario.nome = nome
                usuario.email = email
                usuario.username = email  # Altera o username para o email
                usuario.cpf = cpf
                usuario.telefone = telefone
                usuario.first_name = primeiro_nome
                usuario.last_name = ultimo_nome
                usuario.save()

                # Envia email de confirmação
                send_mail(
                    'Seu perfil foi editado com sucesso!',
                    f'Perfil editado com sucesso, {nome}!\n\nFaça já seus agendamentos de medicamentos.\n\nEntre em contato se não foi você mesmo.\n\nAtenciosamente, Equipe Busca.',
                    'buscapharmatcc@gmail.com',  # Remetente
                    [email],  # Destinatário
                    fail_silently=False,
                )
                messages.success(request, 'Alteração realizada com sucesso!')
                return redirect('home')

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        else:
            messages.error(request, 'Todos os campos devem ser preenchidos.')
    # Para métodos GET, você pode querer renderizar um formulário com dados do usuário
    usuario = get_object_or_404(Usuario, email=request.user.email)  # Obtém o usuário logado
    telefone = request.user.telefone # Assume que o telefone contém o DDD
    ddd_list = [
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "24",
        "27", "28", "31", "32", "33", "34", "35", "37", "38", "41", "42", "43",
        "44", "45", "46", "47", "48", "49", "51", "53", "54", "55", "61", "62",
        "63", "64", "65", "66", "67", "68", "69", "71", "73", "74", "75", "77",
        "79", "81", "82", "83", "84", "85", "86", "87", "88", "89", "91", "92",
        "93", "94", "95", "96", "97", "98", "99"
    ]

    return render(request, 'editar_perfil.html', {'user': usuario, 'telefone': telefone, 'ddd_list': ddd_list})


def editar_perfil_admin(request, username_admin, username_geral):
    admin = get_object_or_404(Admin, username=username_admin)  # Encontra o admin com o username fornecido

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        username = request.POST.get('username')
        partes_nome = nome.split(' ')
        primeiro_nome = partes_nome[0]
        ultimo_nome = partes_nome[-1]

        if nome and email:  # Verifica que os campos estão preenchidos
            try:
                admin.nome = nome
                admin.email = email
                admin.username = username
                admin.first_name = primeiro_nome
                admin.last_name = ultimo_nome
                admin.save()
                messages.success(request, 'Alteração realizada com sucesso!')
                return redirect('home_admin_geral', username=username_geral)
            except Exception as e:
                messages.error(request, f'Erro ao salvar alterações: {e}')
        else:
            messages.error(request, 'Verifique os campos. Todos devem ser preenchidos.')

    return render(request, 'editar_perfil_admin.html', {'username_admin': username_admin, 'username_geral': username_geral, 'admin': admin})





