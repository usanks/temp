from django.contrib import admin
from .models import Prestador, Categoria, Status
# Register your models here.

admin.site.register(Prestador)
admin.site.register(Categoria)
admin.site.register(Status)