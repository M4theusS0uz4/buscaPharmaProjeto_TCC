from tkinter.font import names

from django.contrib import admin
from django.template.context_processors import request
from django.urls import path
from appUsuario import views
from appBusca import views2
from appAdm import views3
from appAgendamento import views4
from appRedefinirSenhaUsuario import views5
from appAdminGeral import views6
from appEditarPerfil import views7
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('busca/', views2.busca, name='busca'),
    path('verificar_existencia/', views.verificar_existencia, name='verificar_existencia'),
    path('busca/medicamento/<int:id_item>/', views2.medicamento, name='medicamento'),
    path('localizar_remedio/<int:id_item>/', views2.localizarMedicamento, name='localizar_remedio'),
    path('cadastro_admin/<int:id_unidade>/<str:username_admin>/', views3.cadastro_adm, name='cadastro_admin'),
    path('login_admin/', views3.login_adm, name='login_admin'),
    path('agendar/<int:id_item>/<int:id_unidade>', views4.agendar , name='agendar'),
    path('horarios_disponiveis/<int:id_unidade>',views4.horarios_disponiveis, name='horarios_disponiveis'),
    path('redefinir_senha/',views5.redefinir_senha, name='redefinir_senha'),
    path('verificar_codigo/<str:email>/',views5.verificar_codigo, name = 'verificar_codigo'),
    path('nova_senha/<str:email>/',views5.nova_senha, name='nova_senha'),
    path('horarios_agendados/',views4.horarios_agendados,name='horarios_agendados'),
    path('cancelar_agendamento/<int:id_agend>/',views4.cancelar_agendamento,name='cancelar_agendamento'),
    path('home_admin/<int:id_admin>/',views3.home_admin, name='home_admin'),
    path('relatorio/<int:id_unidade>/<int:id_admin>/',views3.relatorio_produtos_interesse,name='relatorio_produtos_interesse'),
    path('marcar_realizado/<int:id_agendamento>/<int:id_admin>/',views3.marcar_realizado,name='marcar_realizado'),
    path('relatorio_agendamentos_realizados/<int:id_unidade>/<int:id_admin>/',views3.relatorio_agendamentos_realizados, name='relatorio_agendamentos_realizados'),
    path('login_admin_geral/', views6.login_adm_geral, name='login_admin_geral'),
    path('criar_admin/<str:senha>',views6.criar_admin, name='criar_admin'),
    path('home_admin_geral/<str:username>/',views6.home_admin_geral, name='home_admin_geral'),
    path('editar_perfil_usuario/', views7.editar_perfil_usuario,name='editar_perfil_usuario'),
    path('cria_evento/<str:username>/<int:id_unidade>/',views6.criar_evento,name='cria_evento'),
    path('salvar_evento/<str:username>/',views6.salvar_evento,name='salvar_evento'),
    path('logout/',views.logout_usuario,name='logout_usuario'),
    path('editar_perfil_admin/<str:username_admin>/<str:username_geral>/',views7.editar_perfil_admin, name ='editar_perfil_admin'),
]
