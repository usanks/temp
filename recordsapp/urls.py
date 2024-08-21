from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="recordsapp"),
    path('add-records', views.add_record, name="add-records"),
    path('visitante_edit/<int:id>', views.visitante_edit, name="visitante_edit"),
    path('visitante_delete/<int:id>', views.visitante_delete, name="visitante_delete"),
    path('search_visitantes', csrf_exempt(views.search_visitantes), name="visitante_edit"),
]