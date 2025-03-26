from django.contrib.auth.models import AbstractUser
from django.db import models
from appBusca.models import Unidade
from appAdm.models import Admin
from appBusca.models import Item,Unidade

class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True,db_column='id_evento')
    titulo = models.TextField(max_length=300,db_column='titulo')
    id_item = models.ForeignKey(Item,on_delete=models.CASCADE, db_column='id_item')
    id_unidade = models.ForeignKey(Unidade,on_delete=models.CASCADE, db_column='id_unidade')
    descricao = models.TextField(max_length=255,db_column='descricao')
    data_inicio = models.DateTimeField(db_column='data_inicio')
    data_termino = models.DateTimeField(db_column='data_termino')
    class Meta:
        db_table = 'evento'


