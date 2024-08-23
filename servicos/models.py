from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Create your models here.
class Prestador(models.Model):

    nome = models.TextField()
    cpf = models.CharField(max_length=20)
    categoria = models.CharField(max_length=255)
    empresa = models.TextField()
    placa = models.TextField(null=True, blank=True)
    hora = models.TimeField(default=now)
    data = models.DateField(default=now)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.categoria
    
    def __str__(self):
        return self.status
    
    class Meta:
        ordering = ['status','-data',]
        verbose_name_plural = 'Prestadores de serviço'

class Categoria(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Status'
