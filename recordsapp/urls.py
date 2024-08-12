from django.urls import path
from . import views
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="recordsapp"),
    path('add-records', views.add_record, name="add-records"),
    path('visitante_edit/<int:id>', views.visitante_edit, name="visitante_edit"),
    path('visitante_delete/<int:id>', views.visitante_delete, name="visitante_delete"),
    # path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    # path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    # path('search-expenses', csrf_exempt(views.search_expenses), name="search_expenses"),
    # path('export_csv', views.export_csv, name="export-csv"),
    # path('export_excel', views.export_excel, name="export-excel")
]