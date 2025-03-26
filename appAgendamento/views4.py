from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from appAgendamento.models import Agendamento
from appBusca.models import Unidade, Item
from appBusca.views2 import pegar_endereco_por_cep_e_numero
from appUsuario.models import Usuario


# Create your views here.
@login_required(login_url='login')
def agendar(request, id_item, id_unidade):
    unidade_info = get_object_or_404(Unidade, id_unidade=id_unidade)
    item = Item.objects.get(id_item=id_item)  # Ajuste de acordo com seu modelo
    abertura = unidade_info.hora_abertura.strftime("%H:%M")
    fechamento = unidade_info.hora_encerramento.strftime("%H:%M")

    # Renderize a página de agendamento, passando a unidade e o item selecionado
    if request.method == 'POST':
        data_json = json.loads(request.body)  # Decodifica o JSON
        data = data_json.get('data')  # Acessa o campo 'data'
        hora = data_json.get('hora')

        # Verifica se a data é menor que a data atual
        today = timezone.now().date()
        horario_atual = timezone.localtime().time()
        data_max = today + timedelta(days=365)
        if data < today.strftime('%Y-%m-%d') or (
                hora < horario_atual.strftime('%H:%M') and data < today.strftime('%Y-%m-%d')):
            return JsonResponse(
                {'status': 'error', 'message': 'Data inválida. Não é possível agendar para datas passadas.'},
                status=400
            )
        if data > data_max.strftime('%Y-%m-%d'):
            return JsonResponse(
                {'status': 'error', 'message': 'Data inválida. Não é possível agendar para datas posteriores a um ano'},
                status=400
            )

        # Verifica se já existe um agendamento para a mesma data e hora
        agendamento_existente = Agendamento.objects.filter(data=data, hora=hora, id_item=id_item,
                                                           id_unidade=id_unidade, status='Agendado').exists()

        if agendamento_existente:
            return JsonResponse({'status': 'error', 'message': 'Já existe um agendamento para este horário.'},
                                status=400)

        # Verifica se existe um agendamento cancelado para o mesmo item e unidade
        agendamento_cancelado = Agendamento.objects.filter(data=data, hora=hora, id_item=id_item,
                                                           id_unidade=id_unidade, status='Cancelado').first()

        # Verifica se o horário está dentro do intervalo permitido
        if abertura <= hora <= fechamento:
            if agendamento_cancelado:
                # Atualiza o agendamento cancelado
                agendamento_cancelado.status = 'Agendado'  # Altera o status
                agendamento_cancelado.cpf = request.user  # Atualiza o usuário se necessário
                agendamento_cancelado.save()
            else:
                # Cria um novo agendamento
                novo_agendamento = Agendamento(id_item=item, id_unidade=unidade_info, cpf=request.user, data=data,
                                               hora=hora)
                novo_agendamento.save()

            data_br = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')
            # Envio de email após salvar um novo agendamento
            email = request.user.email
            send_mail(
                'Agendamento realizado com sucesso!',
                f'Agendamento referente ao Dia: {data_br}, Horário: {hora}\n\nRealizado com sucesso!\n\nMedicamento: {item.nome_item}\n\nUnidade: {unidade_info.nome}\n\nCompareça ao local e informe seu nome para uma possível retirada.\n\nSe caso não for comparecer, pedimos que cancele seu agendamento!\n\n att.Equipe Busca.',
                'buscapharmatcc@gmail.com',  # Remetente
                [email],  # Destinatário
                fail_silently=False,
            )
            # Retornar uma resposta JSON para requisição AJAX
            return JsonResponse({'status': 'success', 'message': 'Agendamento realizado com sucesso!'})

        # Caso o horário esteja fora do intervalo permitido
        return JsonResponse({'status': 'error', 'message': 'O horário selecionado está fora do intervalo permitido.'},
                            status=400)

    today = timezone.now().date()
    return render(request, 'janela_agendar.html', {
        'unidade': unidade_info,
        'item': item,
        'abertura': abertura,
        'fechamento': fechamento,
        'today': today,
    })


def horarios_disponiveis(request,id_unidade):
    data = request.GET.get('data')  # Pega a data da requisição GET
    horario_atual = timezone.localtime().time()
    # Consulta no banco para pegar os horários já agendados para aquela data
    agendamentos = Agendamento.objects.filter(data=data,status__in=['Agendado', 'Realizado'],id_unidade=id_unidade).values_list('hora', flat=True)
    # Retorna os horários ocupados
    lista_agendamentos = list(agendamentos)
    unidade_abertura = Unidade.objects.get(id_unidade=id_unidade).hora_abertura
    hora_atual_int = int(horario_atual.strftime('%H'))
    hora_abertura_int = int(unidade_abertura.strftime('%H'))

    hoje = timezone.now().date()
    data_solicitada = timezone.datetime.strptime(data, '%Y-%m-%d').date()

    if data_solicitada == hoje:
        hora_atual_str = f'{hora_atual_int:02}:00:00'
        lista_agendamentos.append(hora_atual_str)
        while hora_abertura_int < hora_atual_int:
            hora_atual_int -= 1
            hora_atual_str = f'{hora_atual_int:02}:00:00'
            lista_agendamentos.append(hora_atual_str)
    return JsonResponse({
        'horarios_ocupados': lista_agendamentos
    })
@login_required(login_url='login')
def horarios_agendados(request):
    agendamentos = Agendamento.objects.filter(cpf=request.user,status='Agendado').select_related('id_item','id_unidade')
    agendamentos_e_endereco = []
    for agendamento in agendamentos:
        cep = agendamento.id_unidade.cep
        numero = agendamento.id_unidade.numero

        endereco_unidade = pegar_endereco_por_cep_e_numero(cep, numero)

        agendamentos_e_endereco.append({'agendamento':agendamento, 'endereco':endereco_unidade})

    return render(request, 'agendamentos.html/',{'agendamentos_e_endereco':agendamentos_e_endereco})



@login_required(login_url='login')
def cancelar_agendamento(request, id_agend):
    agendamento = get_object_or_404(Agendamento, id_agendamento=id_agend, cpf=request.user)
    if request.method == 'POST':
        agendamento.status = 'Cancelado'
        agendamento.save()
        return JsonResponse({'status': 'success', 'message': 'Agendamento cancelado com sucesso!'})

    return JsonResponse({'status': 'error', 'message': 'Erro ao tentar cancelar o agendamento.'}, status=400)