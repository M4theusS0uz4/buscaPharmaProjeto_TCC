from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from appBusca.models import Unidade

class Admin(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administrador_groups',  # Nome único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administrador_permissions',  # Nome único
        blank=True
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    id_unidade  = models.ForeignKey(Unidade, on_delete=models.CASCADE, db_column='id_unidade')
    id_admin = models.IntegerField(primary_key=True, db_column= 'id_adm')
    class Meta:
        db_table = 'administrador'


