from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from appBusca.models import Unidade
class Usuario(AbstractUser):
    # Definindo o related_name para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # Nome único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Nome único
        blank=True
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True,primary_key=True,db_column='cpf')
    username = models.EmailField(max_length=150, unique=True)
    class Meta:
        db_table = 'usuario'
