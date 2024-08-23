from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="servico"),
    path('add-servico', views.add_servico, name="add-servico"),
    path('servico_edit/<int:id>', views.servico_edit, name="servico_edit"),
    path('servico_delete/<int:id>', views.servico_delete, name="servico_delete"),
    path('search_servico', csrf_exempt(views.search_servico), name="servico_edit"),
]
