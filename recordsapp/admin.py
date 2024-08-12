from django.contrib import admin
from .models import Visitante, Categoria, Status
# Register your models here.

admin.site.register(Visitante)
admin.site.register(Categoria)
admin.site.register(Status)
