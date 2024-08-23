from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="fornecedor"),
    path('add-fornecedor', views.add_fornecedor, name="add-fornecedor"),
    path('fornecedor_edit/<int:id>', views.fornecedor_edit, name="fornecedor_edit"),
    path('fornecedor_delete/<int:id>', views.fornecedor_delete, name="fornecedor_delete"),
    path('search_fornecedor', csrf_exempt(views.search_fornecedor), name="fornecedor_edit"),
]
