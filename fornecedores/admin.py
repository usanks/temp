from django.contrib import admin
from .models import Fornecedor, Categoria, Status
# Register your models here.

admin.site.register(Fornecedor)
admin.site.register(Categoria)
admin.site.register(Status)